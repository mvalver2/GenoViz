import pandas as pd
import matplotlib.pyplot as plt



#load and clean files
def load_23andme(file_path):
    df = pd.read_csv(
        file_path,
        sep="\t",
        comment="#",  
        names=["rsid", "chromosome", "position", "genotype"],
        dtype=str
    )
    df = df.dropna()
    return df

user1 = load_23andme("user_info/user_1.txt")
user2 = load_23andme("user_info/user_2.txt")

#merge on shared SNPs
merged = user1.merge(user2, on="rsid", suffixes=("_1", "_2"))
print("Shared SNP count:", len(merged))

#compute overall match rate
def normalize(g):
    return "".join(sorted(g)) 

merged["norm1"] = merged["genotype_1"].apply(normalize)
merged["norm2"] = merged["genotype_2"].apply(normalize)

merged["match"] = merged["norm1"] == merged["norm2"]

overall_match_rate = merged["match"].mean()
print("Overall match rate:", overall_match_rate)


#per chromosome match rates
chrom_match = merged.groupby("chromosome_1")["match"].mean()
print(chrom_match)


# Plot per-chromosome match rate
chrom_match = merged.groupby("chromosome_1")["match"].mean()

plt.figure(figsize=(12,6))
plt.bar(chrom_match.index, chrom_match.values)
plt.xlabel("Chromosome")
plt.ylabel("Match Rate")
plt.title("Per-Chromosome SNP Match Rate Between Two Users")
plt.xticks(rotation=90)
plt.tight_layout()

plt.savefig("results/chromosome_match_rate.png", dpi=300)
plt.show()
