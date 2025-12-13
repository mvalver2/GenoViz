import pandas as pd
import matplotlib.pyplot as plt
import textwrap

# Load data
snps_df = pd.read_csv("rsID/table_trait.csv")
user_df = pd.read_csv(
    "user_info/e_user_1.txt",
    comment="#",
    sep="\t",
    names=["rsid", "chrom", "pos", "genotype"]
)

# Clean IDs
snps_df["rsid"] = snps_df["rsid"].str.strip()
user_df["rsid"] = user_df["rsid"].str.strip()

# YES/NO column
snps_df["user_has_variant"] = snps_df["rsid"].isin(user_df["rsid"]).map({True: "YES", False: "NO"})

# Final table
final = snps_df[["rsid", "gene", "trait", "user_has_variant"]].copy()

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""

    res = []

    for i in range(0, len(lst), n):
        res.append(lst[i:i + n])
    return res

print(chunks("This is a test of something that i think is kinda cool!! Wow!!".split(" "), 5))
# === WRAP LONG TEXT ===
final["trait"] = final["trait"].apply(lambda x: "\n".join([" ".join(chunks(x.split(" "), 4)[i]) for i in range(len(chunks(x.split(" "), 4)))] ))

# --- Generate Image ---
plt.figure(figsize=(12, len(final) * 0.5 + 1))
plt.axis("off")

table = plt.table(
    cellText=final.values,
    colLabels=final.columns,
    colWidths=[0.2, 0.15, 0.5, 0.15],
    loc="center",
)

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 4.0)

plt.savefig("user_yes_no_table.png", bbox_inches="tight", dpi=300)
plt.close()
