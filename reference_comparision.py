import pandas as pd
import allel
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------
# Load user SNP file
# ---------------------------
user_file = "user_snps_chr22.csv"
user_df = pd.read_csv(user_file)
print("First few SNPs in user file:")
print(user_df.head())

# Filter for chromosome 22
user_chr22 = user_df[user_df['chromosome'].astype(str) == '22'].copy()

# ---------------------------
# Load VCF
# ---------------------------
vcf_file = "chr22_subset.vcf.gz"
callset = allel.read_vcf(vcf_file, fields=['variants/CHROM', 'variants/POS', 'variants/ID', 'calldata/GT', 'samples'])
vcf_samples = callset['samples']

vcf_df = pd.DataFrame({
    'chromosome': callset['variants/CHROM'],
    'position': callset['variants/POS'],
    'rsid': callset['variants/ID']
})

gt_array = allel.GenotypeArray(callset['calldata/GT'])

# ---------------------------
# Match user SNPs to VCF
# ---------------------------
vcf_df['key'] = vcf_df['chromosome'].astype(str) + ':' + vcf_df['position'].astype(str)
user_chr22['key'] = user_chr22['chromosome'].astype(str) + ':' + user_chr22['position'].astype(str)

matching_keys = set(vcf_df['key']).intersection(set(user_chr22['key']))
if len(matching_keys) == 0:
    raise ValueError("No matching chr22 SNPs found in VCF. Check your files.")

vcf_idx = [i for i, k in enumerate(vcf_df['key']) if k in matching_keys]
vcf_sub_df = vcf_df.iloc[vcf_idx].copy()
gt_sub = gt_array.take(vcf_idx, axis=0)

# Convert genotypes to dosage (number of alt alleles)
dosage_df = pd.DataFrame(gt_sub.to_n_alt(), columns=vcf_samples)
dosage_df['key'] = vcf_sub_df['key'].values

# Merge user SNPs with dosages
merged = user_chr22.merge(dosage_df, on='key', how='left')
print("Merged SNPs with dosage (first 5 rows):")
print(merged.head())

# ---------------------------
# Load population panel
# ---------------------------
panel_file = "integrated_call_samples_v3.20130502.ALL.panel"
superpop_df = pd.read_csv(panel_file, sep='\t')

# Keep only the samples that exist in the VCF
superpop_df = superpop_df[superpop_df['sample'].isin(vcf_samples)]

# ---------------------------
# Calculate population allele frequencies
# ---------------------------
pop_cols = superpop_df['sample'].tolist()
merged['pop_mean'] = merged[pop_cols].mean(axis=1)

# ---------------------------
# Simple visualization
# ---------------------------
plt.figure(figsize=(10,6))
sns.histplot(merged['pop_mean'], bins=30, kde=True)
plt.axvline(merged[vcf_samples[0]].mean(), color='red', linestyle='--', label='User mean dosage')
plt.xlabel("Allele dosage in population")
plt.ylabel("Number of SNPs")
plt.title("Comparison of user chr22 SNPs to 1000 Genomes population")
plt.legend()
plt.tight_layout()
plt.show()

# Save merged table for reference
merged.to_csv("merged_chr22_dosage_with_pop.csv", index=False)
print("Merged table saved as 'merged_chr22_dosage_with_pop.csv'")