import pandas as pd
from cyvcf2 import VCF
import seaborn as sns
import matplotlib.pyplot as plt

# Load population info
pop_info = pd.read_csv("integrated_call_samples_v3.20130502.ALL.panel", sep="\t")
print(pop_info.head())

# Load the user's matched SNPs
individual = pd.read_csv("chr22_user1_matched.txt", sep="\t")
user_rsids = set(individual['rsid'])  # create a set for fast lookup

# Open VCF
vcf = VCF("chr22_filtered.vcf.gz")

# Extract only SNPs that match the user
records = []
for variant in vcf:
    if variant.ID not in user_rsids:  # <-- FILTER STEP
        continue
    for i, gt in enumerate(variant.genotypes):  # gt = [allele1, allele2, phased]
        records.append({
            "rsid": variant.ID,
            "sample": vcf.samples[i],
            "gt": gt[0] + gt[1]  # simple sum of alleles, 0,1,2
        })

vcf_df = pd.DataFrame(records)
vcf_df = vcf_df.merge(pop_info, left_on="sample", right_on="sample")
print(vcf_df.head())

# Merge on rsid with user's data
merged = vcf_df.merge(individual, on="rsid", suffixes=('_pop','_user'))
print(merged.head())

# Calculate mean difference from population
pop_diff = merged.groupby("super_pop").apply(
    lambda df: (df['gt_user'] - df['gt_pop']).abs().mean()
)
print(pop_diff)

# Allele frequency per SNP in each population
allele_freq = merged.groupby(['rsid','super_pop'])['gt_pop'].mean() / 2
merged = merged.merge(allele_freq.reset_index().rename(columns={'gt_pop':'AF'}), on=['rsid','super_pop'])
rare_variants = merged[merged['AF'] < 0.01]

# Plot mean differences
pop_diff.plot(kind='bar')
plt.ylabel("Mean genotype difference")
plt.title("Similarity of Individual to Populations")
plt.show()

# Plot rare variant counts
rare_counts = rare_variants.groupby('super_pop')['rsid'].count()
rare_counts.plot(kind='bar')
plt.ylabel("Number of rare SNPs")
plt.title("Rare variants in each population")
plt.show()
