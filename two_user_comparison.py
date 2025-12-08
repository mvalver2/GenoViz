import pandas as pd
import matplotlib.pyplot as plt
import json 

def load_23andme_txt(filepath):
    df = pd.read_csv(
        filepath,
        sep="\t",
        comment="#",
        names=["SNP", "chromosome", "position", "genotype"],
        dtype=str
    )
    df.dropna(inplace=True)
    return df


# IBS calculation (0, 1, or 2 shared alleles)
def ibs(g1, g2):
    g1 = str(g1).upper()
    g2 = str(g2).upper()
    bad = ["", "N", "NA", "0", "--", "nan", "NONE"]
    if g1 in bad or g2 in bad:
        return None
    if len(g1) != 2 or len(g2) != 2:
        return None
    a1, a2 = g1[0], g1[1]
    b1, b2 = g2[0], g2[1]

    matches = 0
    if a1 == b1 or a1 == b2:
        matches += 1
    if a2 == b1 or a2 == b2:
        matches += 1

    return matches
user1 = load_23andme_txt("user_info/user_1.txt")
user2 = load_23andme_txt("user_info/user_2.txt")

print("Loaded User1 SNPs:", len(user1))
print("Loaded User2 SNPs:", len(user2))


# Merge on shared SNPs
merged = user1.merge(user2, on="SNP", suffixes=("_1", "_2"))
print("Shared SNP count:", len(merged))


# Compute IBS values
merged["IBS"] = merged.apply(
    lambda r: ibs(r["genotype_1"], r["genotype_2"]),
    axis=1
)
merged_clean = merged.dropna(subset=["IBS"]).copy()

print("Comparable SNPs after filtering:", len(merged_clean))
merged_clean["IBS_normalized"] = merged_clean["IBS"] / 2
ibs_mean = merged_clean["IBS"].mean()

ibs2 = (merged_clean["IBS"] == 2).sum()
ibs1 = (merged_clean["IBS"] == 1).sum()
ibs0 = (merged_clean["IBS"] == 0).sum()

print("\n=== IBS Summary ===")
print("Mean raw IBS (0–2):", round(ibs_mean, 4))
print("Mean normalized IBS (0–1):", round(ibs_mean/2, 4))
print("IBS=2 (perfect match):", ibs2)
print("IBS=1 (partial match):", ibs1)
print("IBS=0 (no match):", ibs0)

total_snps = ibs2 + ibs1 + ibs0
overall_similarity_pct = round(((ibs2 * 2) + ibs1) / (total_snps * 2) * 100, 2)

print("\nOverall Genomic Similarity:", overall_similarity_pct, "%")

# Per-chromosome IBS
merged_clean.loc[:, "chromosome_1"] = merged_clean["chromosome_1"].astype(str)

def chr_sort_key(c):
    if c.isdigit():
        return (0, int(c))
    return (1, c)

chrom_ibsm = (
    merged_clean.groupby("chromosome_1")["IBS_normalized"]
    .mean()
    .sort_index(key=lambda x: x.map(chr_sort_key))
)

# ---- Create JSON data for Plotly (per-chromosome IBS) ----
chromosomes = chrom_ibsm.index.tolist()          # e.g. ["1","2",...,"22","X"]
avg_ibs = chrom_ibsm.values.tolist()             # list of floats

ibs_json = {
    "overall_similarity_pct": overall_similarity_pct,  # 83.08, etc.
    "data": [
        {
            "type": "bar",
            "x": chromosomes,
            "y": avg_ibs,
            "name": "Per-Chromosome IBS Between User1 and User2"
        }
    ],
    "layout": {
        "title": "Per-Chromosome IBS Between User1 and User2",
        "xaxis": {"title": "Chromosome"},
        "yaxis": {"title": "Average IBS (0–1)", "range": [0, 1]}
    }
}

# Write JSON file
with open("results/two_user_IBS_plot.json", "w") as f:
    json.dump(ibs_json, f)

print("Saved: results/two_user_IBS_plot.json")



plt.figure(figsize=(14, 6))
plt.bar(chrom_ibsm.index, chrom_ibsm.values)
plt.ylim(0, 1)  
plt.xlabel("Chromosome")
plt.ylabel("Average IBS (0–1)")
plt.suptitle("Per-Chromosome IBS Between User1 and User2", fontsize=16, fontweight="heavy")
plt.title(f"Overall Similarity: {overall_similarity_pct}%", fontsize=13, fontweight = "bold")
plt.xticks(rotation=90)

plt.tight_layout()

plt.savefig("results/two_user_IBS_output.png", dpi=300)
plt.show()
print("\nSaved: results/two_user_IBS_output.png")
merged_clean.to_csv("results/two_user_IBS_output.csv", index=False)
print("Saved: results/two_user_IBS_output.csv")
