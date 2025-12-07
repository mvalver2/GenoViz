import pandas as pd
import allel
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import os
import json

# --------------------------
# File paths
# --------------------------
USER_FILE = "Individual1Genomics.txt"
PANEL_FILE = "integrated_call_samples_v3.20130502.ALL.panel"
VCF_FILE = "chr22_subset.vcf.gz"
OUTPUT_DIR = "results"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------------
# Load user 23andMe file
# --------------------------
print(f"Loading user file: {USER_FILE}")
user_df = pd.read_csv(USER_FILE, sep='\t', comment='#', low_memory=False)

col_map = {
    user_df.columns[0]: 'rsid',
    user_df.columns[1]: 'chromosome',
    user_df.columns[2]: 'position',
    user_df.columns[3]: 'genotype'
}
user_df = user_df.rename(columns=col_map)

print("Columns detected:", user_df.columns.tolist())

# Filter chr22
user_chr22 = user_df[user_df['chromosome'].astype(str) == '22'].copy()
print(f"Total user SNPs (chr22): {len(user_chr22)}")


# --------------------------
# Load 1000 Genomes panel
# --------------------------
panel = pd.read_csv(PANEL_FILE, sep='\t', comment='#', low_memory=False)
panel = panel[['sample','pop','super_pop','gender']].dropna()

# --------------------------
# Load VCF – get ALL sample names
# --------------------------
print("Reading VCF sample list...")
vcf_header = allel.read_vcf(VCF_FILE, fields=['samples'])
vcf_samples = vcf_header['samples']

# Use ALL samples present in the VCF
reduced_panel = panel[panel['sample'].isin(vcf_samples)].reset_index(drop=True)

print("Super-pop counts (ALL samples):")
print(reduced_panel['super_pop'].value_counts())
print("Total VCF samples:", len(reduced_panel))


# --------------------------
# Load VCF FULL GT data
# --------------------------
print(f"Opening full VCF: {VCF_FILE}")
callset = allel.read_vcf(
    VCF_FILE,
    samples=vcf_samples.tolist(),   # ALL samples
    fields=[
        'variants/CHROM','variants/POS','variants/ID','variants/REF','variants/ALT',
        'calldata/GT','samples'
    ]
)

vcf_df = pd.DataFrame({
    'chromosome': callset['variants/CHROM'],
    'position': callset['variants/POS'],
    'rsid': callset['variants/ID'],
    'ref': callset['variants/REF'],
    'alt': [alt[0] for alt in callset['variants/ALT']]
})

gt_array = allel.GenotypeArray(callset['calldata/GT'])

# --------------------------
# Match SNPs
# --------------------------
user_chr22['key'] = user_chr22['chromosome'].astype(str) + ':' + user_chr22['position'].astype(str)
vcf_df['key'] = vcf_df['chromosome'].astype(str) + ':' + vcf_df['position'].astype(str)

matching_keys = set(vcf_df['key']).intersection(set(user_chr22['key']))
print(f"Found {len(matching_keys)} matched SNP positions.")

vcf_idx = [i for i, k in enumerate(vcf_df['key']) if k in matching_keys]
vcf_sub_df = vcf_df.iloc[vcf_idx].copy()
gt_sub = gt_array.take(vcf_idx, axis=0)

# Convert reference sample genotypes to dosage
dosage_df = pd.DataFrame(
    gt_sub.to_n_alt(), 
    columns=vcf_samples
)
dosage_df['key'] = vcf_sub_df['key'].values


# --------------------------
# PCA – user dosage alignment
# --------------------------
def genotype_to_dosage(gt, ref, alt):
    if not isinstance(gt, str) or len(gt) != 2:
        return np.nan
    alleles = list(gt.upper())
    dosage = sum(a == alt for a in alleles)
    # treat nonmatching as missing
    if any((a not in [ref, alt]) for a in alleles):
        return np.nan
    return dosage

user_dosage = []
for i, row in vcf_sub_df.iterrows():
    k = row['key']
    g = user_chr22.loc[user_chr22['key']==k, 'genotype']
    if g.empty:
        user_dosage.append(np.nan)
        continue
    
    g_str = g.values[0]
    ref_v = row['ref'].upper()
    alt_v = row['alt'].upper()
    a1, a2 = g_str[0].upper(), g_str[1].upper()

    # Exact or flipped match
    if {a1, a2} == {ref_v, alt_v}:
        # aligned or reversed order
        dosage = genotype_to_dosage(g_str, ref_v, alt_v)
    else:
        dosage = np.nan

    user_dosage.append(dosage)

user_dosage = np.array(user_dosage)

# --------------------------
# Build PCA matrix
# --------------------------
pca_matrix = dosage_df[vcf_samples].to_numpy().T  # samples x SNP
pca_matrix = np.vstack([pca_matrix, user_dosage]) # add user

# Fill missing values (per SNP mean excluding user)
col_mean = np.nanmean(pca_matrix[:-1, :], axis=0)
for r, c in zip(*np.where(np.isnan(pca_matrix))):
    pca_matrix[r, c] = col_mean[c]

# Standardize
scaler = StandardScaler()
pca_matrix_std = scaler.fit_transform(pca_matrix)

# PCA
pca = PCA(n_components=2)
pcs = pca.fit_transform(pca_matrix_std)

# Build JSON output for React dashboard
pca_output = []

# All 1000 Genomes samples
for i, sample in enumerate(vcf_samples):
    pca_output.append({
        "sample": sample,
        "super_pop": reduced_panel.loc[reduced_panel['sample']==sample, 'super_pop'].values[0],
        "pop": reduced_panel.loc[reduced_panel['sample']==sample, 'pop'].values[0],
        "gender": reduced_panel.loc[reduced_panel['sample']==sample, 'gender'].values[0],
        "pc1": float(pcs[i,0]),
        "pc2": float(pcs[i,1]),
        "cluster": None    # (Optional, add later)
    })

# Add user point
pca_output.append({
    "sample": "USER",
    "super_pop": "User",
    "pop": "User",
    "gender": "Unknown",
    "pc1": float(pcs[-1,0]),
    "pc2": float(pcs[-1,1]),
    "cluster": "USER_CLUSTER"
})

# Save JSON
with open(os.path.join(OUTPUT_DIR, "pca_points.json"), "w") as f:
    json.dump(pca_output, f, indent=2)

print("Saved interactive PCA JSON: results/pca_points.json")

# --------------------------
# Plot PCA
# --------------------------
plt.figure(figsize=(10,8))
superpop_colors = {
    "AFR": "blue",
    "AMR": "orange",
    "EAS": "green",
    "EUR": "purple",
    "SAS": "brown"
}

for spop in superpop_colors.keys():
    idx = reduced_panel[reduced_panel['super_pop'] == spop].index
    plt.scatter(pcs[idx,0], pcs[idx,1], c=superpop_colors[spop], s=40, label=spop, alpha=0.7)

# Plot user
plt.scatter(
    pcs[-1,0], pcs[-1,1],
    c="red", marker="*", s=400, edgecolor="black", label="User"
)

plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("PCA of chr22 — 1000 Genomes (ALL samples) + User")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "pca_all_samples_user.png"))
plt.close()
print("Saved PCA plot with ALL samples.")


# --------------------------
# Boxplot: allele dosage by super-pop
# --------------------------
box_data = []
labels = []

for spop in reduced_panel['super_pop'].unique():
    spop_samples = reduced_panel[reduced_panel['super_pop']==spop]['sample']
    box_data.append(dosage_df[spop_samples].values.flatten())
    labels.append(spop)

plt.figure(figsize=(10,6))
plt.boxplot(box_data, labels=labels)
plt.ylabel("Allele dosage (0,1,2)")
plt.title("Allele Dosages by Super-Population — chr22")
plt.savefig(os.path.join(OUTPUT_DIR, "boxplot_all_samples.png"))
plt.close()

print("Saved dosage boxplot with all samples.")
