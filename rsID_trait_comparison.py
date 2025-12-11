import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------------------------------
# 1. LOAD 23andMe DATA
# -----------------------------------------------------
user = pd.read_csv(
    "user_info/user_1.txt",
    comment='#',
    sep='\t',
    names=["rsid", "chrom", "pos", "genotype"]
)

# Clean RSIDs and genotypes
user["rsid"] = user["rsid"].astype(str).str.strip()
user["genotype"] = user["genotype"].astype(str).str.strip()

# Convert "--" to NaN (VERY IMPORTANT)
user["genotype"].replace("--", pd.NA, inplace=True)

# Print first few rows to verify
print("\n=== 23andMe FIRST ROWS ===")
print(user.head())
print("\nTotal SNPs in 23andMe:", len(user))


# -----------------------------------------------------
# 2. LOAD YOUR SNP → TRAIT LIST
# -----------------------------------------------------
trait_df = pd.read_csv("rsID/snp_trait.csv")

# Clean rsid column
trait_df["rsid"] = trait_df["rsid"].astype(str).str.strip()

print("\n=== TRAIT LIST ===")
print(trait_df.head())
print("Total SNPs in trait list:", len(trait_df))


# -----------------------------------------------------
# 3. MERGE ON RSID
# -----------------------------------------------------
merged = trait_df.merge(user, on="rsid", how="left")

# Check if found
merged["found"] = merged["genotype"].notna()

print("\n=== MERGED DATA SAMPLE ===")
print(merged.head(15))


# -----------------------------------------------------
# 4. CHECK WHICH SNPs WERE FOUND AND MISSING
# -----------------------------------------------------
found_snps = merged[merged["found"] == True]
missing_snps = merged[merged["found"] == False]

print("\n=== FOUND SNPs ===")
print(found_snps[["rsid", "gene", "trait", "genotype"]])

print("\n=== MISSING SNPs ===")
print(missing_snps[["rsid", "gene", "trait"]])


# -----------------------------------------------------
# 5. CALCULATE PERCENTAGE PER TRAIT
# -----------------------------------------------------
trait_counts = merged.groupby("trait")["found"].mean() * 100

print("\n=== PERCENTAGE PER TRAIT ===")
print(trait_counts)


# -----------------------------------------------------
# 6. PLOT
# -----------------------------------------------------
plt.figure(figsize=(10, 6))
trait_counts.sort_values().plot(kind="barh")
plt.xlabel("Percentage of SNPs Found (%)")
plt.title("Trait Coverage in 23andMe Raw Data")
plt.tight_layout()
plt.show()

import json

# -----------------------------------------------------
# 7. SAVE TRAIT COVERAGE TO JSON
# -----------------------------------------------------
# Convert Series to dictionary
trait_counts_dict = trait_counts.to_dict()

# Save to JSON file
with open("trait_coverage.json", "w") as f:
    json.dump(trait_counts_dict, f, indent=4)

# Optional: print JSON to console
print("\n=== TRAIT COVERAGE JSON ===")
print(json.dumps(trait_counts_dict, indent=4))
