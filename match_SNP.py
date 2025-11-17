import pandas as pd

# Load the 1000 Genomes chr22 filtered table
ref_table = pd.read_csv(
    "chr22_1000G_table.txt",
    sep="\t", 
    names=["rsid","chrom","pos","ref","alt"]
)

# Load 23andMe file, skipping comment lines that start with #
individual = pd.read_csv(
    "Individual1Genomics.txt",
    sep="\t",
    comment='#',  # skip metadata lines starting with #
    names=["rsid","chrom","pos","genotype"],  # give column names
    usecols=[0,1,2,3]  # only read the first 4 columns
)

# Filter 1000 Genomes table to only SNPs present in the individual's 23andMe file
matched_snps = ref_table[ref_table['rsid'].isin(individual['rsid'])]

# Save matched SNPs to a new file
matched_snps.to_csv("chr22_user1_matched.txt", sep="\t", index=False)

print(f"Number of SNPs matched: {len(matched_snps)}")

