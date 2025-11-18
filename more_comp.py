import pandas as pd
import allel
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import os
from tqdm import tqdm

# --------------------------
# File paths (update as needed)
# --------------------------
USER_FILE = "Individual1Genomics.txt"
PANEL_FILE = "integrated_call_samples_v3.20130502.ALL.panel"
VCF_FILE = "chr22_subset.vcf.gz"
OUTPUT_DIR = "results"
MAX_PER_SUPERPOP = 20

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------------
# Load user 23andMe file
# --------------------------
print(f"Loading user file: {USER_FILE}")
user_df = pd.read_csv(USER_FILE, sep='\t', comment='#', low_memory=False)

# Auto-detect columns and rename
col_map = {
    user_df.columns[0]: 'rsid',
    user_df.columns[1]: 'chromosome',
    user_df.columns[2]: 'position',
    user_df.columns[3]: 'genotype'
}
user_df = user_df.rename(columns=col_map)

print("Columns detected and renamed:", user_df.columns.tolist())
print("First few SNPs in user file:")
print(user_df.head())

# Filter chr22
user_chr22 = user_df[user_df['chromosome'].astype(str) == '22'].copy()
print(f"Total user SNPs (chr22): {len(user_chr22)}")

# --------------------------
# Load 1000 Genomes panel and sample subset
# --------------------------
panel = pd.read_csv(PANEL_FILE, sep='\t', comment='#', low_memory=False)
print("Panel columns before cleaning:", panel.columns.tolist())

panel = panel[['sample','pop','super_pop','gender']].dropna()
reduced_panel = panel.groupby('super_pop', group_keys=False)\
    .apply(lambda g: g.sample(n=min(MAX_PER_SUPERPOP,len(g)), random_state=42))\
    .reset_index(drop=True)
print("Samples chosen per super-pop:\n", reduced_panel['super_pop'].value_counts())
print(f"Total kept samples: {len(reduced_panel)}")

# --------------------------
# Load VCF
# --------------------------
print(f"Opening VCF: {VCF_FILE}")
callset = allel.read_vcf(
    VCF_FILE,
    samples=reduced_panel['sample'].tolist(),
    fields=['variants/CHROM','variants/POS','variants/ID','calldata/GT','samples']
)

vcf_df = pd.DataFrame({
    'chromosome': callset['variants/CHROM'],
    'position': callset['variants/POS'],
    'rsid': callset['variants/ID']
})
gt_array = allel.GenotypeArray(callset['calldata/GT'])
vcf_samples = callset['samples']

# --------------------------
# Match user SNPs to VCF by rsid
# --------------------------
user_rsids = set(user_chr22['rsid'])
vcf_df['key'] = vcf_df['chromosome'].astype(str) + ':' + vcf_df['position'].astype(str)
user_chr22['key'] = user_chr22['chromosome'].astype(str) + ':' + user_chr22['position'].astype(str)

matching_keys = set(vcf_df['key']).intersection(set(user_chr22['key']))
print(f"Found {len(matching_keys)} matching chr22 SNPs in VCF")

vcf_idx = [i for i, k in enumerate(vcf_df['key']) if k in matching_keys]
vcf_sub_df = vcf_df.iloc[vcf_idx].copy()
gt_sub = gt_array.take(vcf_idx, axis=0)

# Dosage conversion (0,1,2)
dosage_df = pd.DataFrame(gt_sub.to_n_alt(), columns=vcf_samples)
dosage_df['key'] = vcf_sub_df['key'].values

# Merge user SNPs with dosages
merged = user_chr22.merge(dosage_df, on='key', how='left')
merged.to_csv(os.path.join(OUTPUT_DIR,'merged_chr22_dosage.csv'), index=False)
print("Merged table saved:", merged.shape)

# --------------------------
# Allele frequencies per super-pop
# --------------------------
af_by_pop = {}
for spop in reduced_panel['super_pop'].unique():
    spop_samples = reduced_panel[reduced_panel['super_pop']==spop]['sample']
    af = dosage_df[spop_samples].sum(axis=1) / (2*len(spop_samples))
    af_by_pop[spop] = af

af_df = pd.DataFrame(af_by_pop)
af_df['rsid'] = vcf_sub_df['rsid'].values
af_df.to_csv(os.path.join(OUTPUT_DIR,'af_by_superpop_chr22.csv'), index=False)
print("Saved allele frequency table.")

# --------------------------
# PCA analysis
# --------------------------
pca_matrix = dosage_df[vcf_samples].to_numpy().T  # samples x variants
pca = PCA(n_components=3)
pcs = pca.fit_transform(pca_matrix)

plt.figure(figsize=(8,6))
for i, spop in enumerate(reduced_panel['super_pop']):
    plt.scatter(pcs[i,0], pcs[i,1], label=spop)
plt.xlabel('PC1'); plt.ylabel('PC2')
plt.title('PCA of chr22: individual vs populations')
plt.legend()
plt.savefig(os.path.join(OUTPUT_DIR,'pca_pop_placement.png'))
plt.close()
print("Saved PCA plot.")

# --------------------------
# Dosage boxplot by super-pop
# --------------------------
box_data = []
labels = []
for spop in reduced_panel['super_pop'].unique():
    spop_samples = reduced_panel[reduced_panel['super_pop']==spop]['sample']
    box_data.append(dosage_df[spop_samples].values.flatten())
    labels.append(spop)

plt.figure(figsize=(10,6))
plt.boxplot(box_data, labels=labels)
plt.ylabel('Allele dosage (0,1,2)')
plt.title('Allele dosages by super-population (chr22)')
plt.savefig(os.path.join(OUTPUT_DIR,'pop_boxplot_dosage.png'))
plt.close()
print("Saved dosage boxplot.")
