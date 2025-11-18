import pandas as pd

# 1. Load the 1000 Genomes chr22 table
ref_table = pd.read_csv(
    "chr22_1000G_table.txt",
    sep="\t",
    names=["rsid", "chrom", "pos", "ref", "alt"]
)

# 2. Load user (23andMe) file, skipping '#' comment lines
individual = pd.read_csv(
    "Individual1Genomics.txt",
    sep="\t",
    comment="#",
    names=["rsid", "chrom", "pos", "genotype"],
    usecols=[0, 1, 2, 3]
)

# OPTIONAL: keep only chr22 in user file if chrom is labeled "22" or "chr22"
# individual = individual[individual["chrom"].astype(str).isin(["22", "chr22"])]

# 3. Match SNPs by rsid (intersection of user and 1000G)
merged = individual.merge(ref_table, on="rsid", how="inner")

# After merge, columns are like:
# rsid, chrom_x, pos_x, genotype, chrom_y, pos_y, ref, alt
# We'll take chrom/pos from 1000G as canonical
merged = merged.rename(columns={"chrom_y": "chrom", "pos_y": "pos"})
merged = merged[["rsid", "chrom", "pos", "ref", "alt", "genotype"]]

# 4. Encode user genotype as 0/1/2 based on ref/alt
def encode_genotype(row):
    gt = str(row["genotype"])
    if len(gt) != 2:
        return pd.NA

    a1, a2 = gt[0], gt[1]
    ref, alt = row["ref"], row["alt"]

    # If genotype alleles aren't ref or alt, drop (ambiguous or multi-alt)
    if (a1 not in [ref, alt]) or (a2 not in [ref, alt]):
        return pd.NA

    # Count how many ALT alleles
    return int((a1 == alt) + (a2 == alt))

merged["gt_user"] = merged.apply(encode_genotype, axis=1)

# Drop rows where we couldn't encode genotype
merged = merged.dropna(subset=["gt_user"])
merged["gt_user"] = merged["gt_user"].astype(int)

# 5. Save matched SNPs to new file
merged.to_csv("chr22_user1_matched.txt", sep="\t", index=False)

print(f"Number of SNPs matched and encoded: {len(merged)}")
