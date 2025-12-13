import pandas as pd
import matplotlib.pyplot as plt
import textwrap
import json

# --------------------------
# Load data
# --------------------------
snps_df = pd.read_csv("rsID/table_trait.csv")

user_df = pd.read_csv(
    "Individual1Genomics.txt",
    comment="#",
    sep="\t",
    names=["rsid", "chrom", "pos", "genotype"],
    low_memory=False
)

# --------------------------
# Clean rsIDs
# --------------------------
snps_df["rsid"] = snps_df["rsid"].astype(str).str.strip()
user_df["rsid"] = user_df["rsid"].astype(str).str.strip()

# --------------------------
# YES / NO if user has SNP
# --------------------------
user_rsids = set(user_df["rsid"])

snps_df["user_has_variant"] = snps_df["rsid"].apply(
    lambda x: "YES" if x in user_rsids else "NO"
)

# --------------------------
# Final table
# --------------------------
final = snps_df[["rsid", "gene", "trait", "user_has_variant"]].copy()

# --------------------------
# Wrap long trait text for plotting
# --------------------------
def wrap_text(text, width=35):
    return "\n".join(textwrap.wrap(text, width))

final["trait"] = final["trait"].apply(lambda x: wrap_text(str(x)))

# --------------------------
# Save JSON for dashboard
# --------------------------
json_output = []

for _, row in final.iterrows():
    json_output.append({
        "rsid": row["rsid"],
        "gene": row["gene"],
        "description": row["trait"].replace("\n", " "),
        "user_has_variant": row["user_has_variant"]
    })

with open("results/user_trait_variants.json", "w") as f:
    json.dump(json_output, f, indent=2)

print("Saved JSON: results/user_trait_variants.json")

# --------------------------
# Generate table image
# --------------------------
plt.figure(figsize=(12, len(final) * 0.5 + 1))
plt.axis("off")

table = plt.table(
    cellText=final.values,
    colLabels=final.columns,
    colWidths=[0.18, 0.15, 0.52, 0.15],
    loc="center"
)

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 4.0)

plt.savefig("results/user_yes_no_table.png", bbox_inches="tight", dpi=300)
plt.close()

print("Saved table image: results/user_yes_no_table.png")
