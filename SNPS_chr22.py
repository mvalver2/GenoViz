import allel
import pandas as pd

# Load VCF
vcf_file = "chr22_subset.vcf.gz"
callset = allel.read_vcf(vcf_file, fields=['variants/CHROM', 'variants/POS', 'variants/ID'])

# Extract chromosome, position, rsid
chrom = callset['variants/CHROM']
pos = callset['variants/POS']
rsid = callset['variants/ID']

# Create DataFrame
snp_df = pd.DataFrame({
    'rsid': rsid,
    'chromosome': chrom,
    'position': pos,
    'genotype': ['NN'] * len(rsid)  # placeholder genotype
})

# Filter for chr22 only (just in case)
snp_df = snp_df[snp_df['chromosome'] == '22']

# Save to CSV
snp_df.to_csv("user_snps_chr22.csv", index=False)
print(f"user_snps_chr22.csv created with {len(snp_df)} SNPs!")
