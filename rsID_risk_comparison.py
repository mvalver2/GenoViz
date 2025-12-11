import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. LOAD 23andMe USER DATA
# ==========================================
user = pd.read_csv(
    "user_info/user_1.txt",
    comment="#",
    sep="\t",
    names=["rsid", "chrom", "pos", "genotype"]
)

user["rsid"] = user["rsid"].astype(str).str.strip()
user["genotype"] = user["genotype"].astype(str).str.strip()
user["genotype"].replace("--", pd.NA, inplace=True)


# ==========================================
# 2. LOAD EXTENDED SNP TRAIT LIST (with risk alleles)
# ==========================================
trait_df = pd.read_csv("rsID/snp_trait_risk.csv")
trait_df["rsid"] = trait_df["rsid"].astype(str).str.strip()
trait_df["risk_allele"] = trait_df["risk_allele"].astype(str).str.upper().str.strip()


# ==========================================
# 3. MERGE DATASETS
# ==========================================
merged = trait_df.merge(user, on="rsid", how="left")
merged["found"] = merged["genotype"].notna()


# ==========================================
# 4. COUNT RISK ALLELES PER SNP
# ==========================================
def count_risk(geno, risk):
    if pd.isna(geno):
        return 0
    return geno.count(risk)

merged["risk_count"] = merged.apply(
    lambda row: count_risk(row["genotype"], row["risk_allele"]),
    axis=1
)


# ==========================================
# 5. SUM RISK PER TRAIT
# ==========================================
risk_per_trait = merged.groupby("trait")["risk_count"].sum()
snps_per_trait = merged.groupby("trait")["risk_count"].count()

# Normalize to 0–100% “risk load”
risk_percentage = (risk_per_trait / (snps_per_trait * 2)) * 100


# ==========================================
# 6. PRINT RESULTS
# ==========================================
print("\n=== SNP-LEVEL RESULTS ===")
print(merged[["rsid", "gene", "trait", "genotype", "risk_allele", "risk_count"]])

print("\n=== RISK % PER TRAIT ===")
print(risk_percentage.sort_values(ascending=False))


# ==========================================
# 7. PLOT RISK LEVEL PER TRAIT
# ==========================================
plt.figure(figsize=(10, 6))
risk_percentage.sort_values().plot(kind="barh")

plt.xlabel("Risk Percentage (%)")
plt.title("User Genetic Risk Load by Trait/Disease")

# Force axis to show 0–100%
plt.xlim(0, 100)

plt.tight_layout()
plt.show()

# ==========================================
# 8. add json file output
# ==========================================
import json

# Convert Series to dictionary
risk_dict = risk_percentage.to_dict()

# Save as JSON file
with open("risk_percentage.json", "w") as f:
    json.dump(risk_dict, f, indent=4)

print("Saved risk percentages to risk_percentage.json")
