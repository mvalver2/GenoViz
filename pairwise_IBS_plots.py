#!/usr/bin/env python3
"""
GenoViz - Pairwise Comparison (Alternatives to Per-Chromosome IBS)

This script keeps your existing 23andMe parsing + IBS matching,
but replaces the critiqued "mean IBS per chromosome" visualization with:

(1) Shared vs Unique SNP counts (coverage overview)
    - X-axis: category (Shared, User1-only, User2-only)
    - Y-axis: count of SNPs

(2) Genotype difference histogram (high-resolution pairwise comparison)
    - X-axis: mismatch severity derived from IBS (0/1/2)
        0 = identical genotype (IBS=2)
        1 = share one allele (IBS=1)
        2 = share zero alleles (IBS=0)
    - Y-axis: count of SNPs in each category

(3) OPTIONAL: Rare differences by super-population (requires AF file)
    - X-axis: super-pop (AFR, AMR, EAS, EUR, SAS)
    - Y-axis: count of SNPs where users differ AND variant is rare in that super-pop

Outputs (into results/ by default):
- two_user_snp_overlap.png + .json + .csv
- two_user_genotype_difference_hist.png + .json + .csv
- OPTIONAL two_user_rare_differences_by_superpop.png + .json + .csv
- two_user_pairwise_variant_table.csv (useful for your dashboard table)
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt


# ----------------------------
# Input helpers (same as yours)
# ----------------------------
def load_23andme_txt(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(
        filepath,
        sep="\t",
        comment="#",
        names=["SNP", "chromosome", "position", "genotype"],
        dtype=str
    )
    df.dropna(inplace=True)
    return df


# IBS calculation (0, 1, or 2 shared alleles) — kept from your script
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


def ensure_results_dir(results_dir: str):
    os.makedirs(results_dir, exist_ok=True)


# ----------------------------
# Plot 1: Shared vs Unique SNPs
# ----------------------------
def plot_snp_overlap(user1: pd.DataFrame, user2: pd.DataFrame, results_dir: str):
    s1 = set(user1["SNP"].astype(str))
    s2 = set(user2["SNP"].astype(str))

    shared = len(s1 & s2)
    u1_only = len(s1 - s2)
    u2_only = len(s2 - s1)

    overlap_df = pd.DataFrame({
        "category": ["Shared SNPs", "User 1 only", "User 2 only"],
        "count": [shared, u1_only, u2_only],
    })

    # JSON (Plotly-style) for Dash integration
    overlap_json = {
        "data": [{
            "type": "bar",
            "x": overlap_df["category"].tolist(),
            "y": overlap_df["count"].tolist(),
            "name": "SNP coverage"
        }],
        "layout": {
            "title": "SNP Coverage Between User1 and User2",
            "xaxis": {"title": "Category"},
            "yaxis": {"title": "Number of SNPs"}
        }
    }

    with open(os.path.join(results_dir, "two_user_snp_overlap.json"), "w") as f:
        json.dump(overlap_json, f)

    # Matplotlib PNG
    plt.figure(figsize=(9, 5))
    plt.bar(overlap_df["category"], overlap_df["count"])
    plt.ylabel("Number of SNPs")
    plt.xlabel("Category")
    plt.title("SNP Coverage Between User1 and User2")
    plt.tight_layout()
    out_png = os.path.join(results_dir, "two_user_snp_overlap.png")
    plt.savefig(out_png, dpi=300)
    plt.close()

    # CSV
    overlap_df.to_csv(os.path.join(results_dir, "two_user_snp_overlap.csv"), index=False)

    return overlap_df


# -----------------------------------------
# Plot 2: Genotype difference (IBS-derived)
# -----------------------------------------
def plot_genotype_difference_hist(merged_clean: pd.DataFrame, results_dir: str):
    """
    Use IBS to define mismatch severity:
      IBS=2 -> diff=0 (identical genotype)
      IBS=1 -> diff=1 (share one allele)
      IBS=0 -> diff=2 (share zero alleles)
    """
    merged_clean = merged_clean.copy()
    merged_clean["diff_level"] = 2 - merged_clean["IBS"].astype(int)

    # Count categories (make sure all bins exist)
    counts = merged_clean["diff_level"].value_counts().reindex([0, 1, 2], fill_value=0)
    diff_df = pd.DataFrame({
        "diff_level": counts.index,
        "count": counts.values
    })
    diff_df["label"] = diff_df["diff_level"].map({
        0: "Δ=0 (same genotype)",
        1: "Δ=1 (share one allele)",
        2: "Δ=2 (share zero alleles)"
    })

    # Plotly-style JSON
    diff_json = {
        "data": [{
            "type": "bar",
            "x": diff_df["label"].tolist(),
            "y": diff_df["count"].tolist(),
            "name": "Genotype difference histogram"
        }],
        "layout": {
            "title": "Genotype Differences Between User1 and User2 (SNP-level)",
            "xaxis": {"title": "Difference category (derived from IBS)"},
            "yaxis": {"title": "Number of SNPs"}
        }
    }
    with open(os.path.join(results_dir, "two_user_genotype_difference_hist.json"), "w") as f:
        json.dump(diff_json, f)

    # Matplotlib PNG
    plt.figure(figsize=(11, 5))
    plt.bar(diff_df["label"], diff_df["count"])
    plt.ylabel("Number of SNPs")
    plt.xlabel("Difference category (derived from IBS)")
    plt.title("Genotype Differences Between User1 and User2 (SNP-level)")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    out_png = os.path.join(results_dir, "two_user_genotype_difference_hist.png")
    plt.savefig(out_png, dpi=300)
    plt.close()

    # CSV
    diff_df.to_csv(os.path.join(results_dir, "two_user_genotype_difference_hist.csv"), index=False)

    return diff_df, merged_clean


# ---------------------------------------------------------
# Plot 3 (OPTIONAL): Rare differences by super-population
# ---------------------------------------------------------
def plot_rare_differences_by_superpop(
    merged_clean: pd.DataFrame,
    af_path: str,
    results_dir: str,
    rare_threshold: float = 0.01
):
    """
    Requires allele frequency (AF) information per SNP and per super-population.

    Expected AF file format (CSV):
      SNP,AFR,AMR,EAS,EUR,SAS
    where each super-pop column is allele frequency (0..1), may include NaN.

    We count SNPs where users differ (IBS < 2) AND AF < rare_threshold for each super-pop.

    Output:
      - two_user_rare_differences_by_superpop.png/.json/.csv
    """
    if not os.path.exists(af_path):
        print(f"[Skip] AF file not found at: {af_path}")
        print("       To enable Plot 3, create a CSV with columns: SNP,AFR,AMR,EAS,EUR,SAS")
        return None

    
    af = pd.read_csv(af_path)

    # Fix column name + order for our AF file
    af = af.rename(columns={"rsid": "SNP"})
    af = af[["SNP", "AFR", "AMR", "EAS", "EUR", "SAS"]]

    # Ensure AF columns are numeric
    for sp in ["AFR", "AMR", "EAS", "EUR", "SAS"]:
        af[sp] = pd.to_numeric(af[sp], errors="coerce")


    required = {"SNP", "AFR", "AMR", "EAS", "EUR", "SAS"}
    if not required.issubset(set(af.columns)):
        print(f"[Skip] AF file exists but is missing required columns: "
              f"{sorted(list(required - set(af.columns)))}")
        return None

    # Focus only on SNPs where users differ at least a bit
    diffs = merged_clean[merged_clean["IBS"].astype(int) < 2].copy()
    diffs["SNP"] = diffs["SNP"].astype(str)

    joined = diffs.merge(af, on="SNP", how="left")

    superpops = ["AFR", "AMR", "EAS", "EUR", "SAS"]
    counts = {}
    for sp in superpops:
        counts[sp] = ((joined[sp].notna()) & (joined[sp].astype(float) < rare_threshold)).sum()

    out_df = pd.DataFrame({
        "super_population": list(counts.keys()),
        "rare_diff_snps_count": list(counts.values())
    })

    # Plotly-style JSON
    out_json = {
        "data": [{
            "type": "bar",
            "x": out_df["super_population"].tolist(),
            "y": out_df["rare_diff_snps_count"].tolist(),
            "name": f"Rare differing SNPs (AF < {rare_threshold})"
        }],
        "layout": {
            "title": f"Rare Differences Between Users by Super-Population (AF < {rare_threshold})",
            "xaxis": {"title": "Super-population"},
            "yaxis": {"title": "Count of differing SNPs that are rare"}
        }
    }
    with open(os.path.join(results_dir, "two_user_rare_differences_by_superpop.json"), "w") as f:
        json.dump(out_json, f)

    # Matplotlib PNG
    plt.figure(figsize=(8, 5))
    plt.bar(out_df["super_population"], out_df["rare_diff_snps_count"])
    plt.ylabel("Count of rare differing SNPs")
    plt.xlabel("Super-population")
    plt.title(f"Rare Differences Between Users by Super-Population (AF < {rare_threshold})")
    plt.tight_layout()
    out_png = os.path.join(results_dir, "two_user_rare_differences_by_superpop.png")
    plt.savefig(out_png, dpi=300)
    plt.close()

    # CSV
    out_df.to_csv(os.path.join(results_dir, "two_user_rare_differences_by_superpop.csv"), index=False)

    return out_df


# ----------------------------
# Main
# ----------------------------
def main():
    user1_path = "Individual1Genomics.txt"
    user2_path = "Individual2Genomics.txt"
    results_dir = "results"
    af_path = "results/af_by_superpop_chr22.csv"

    ensure_results_dir(results_dir)

    user1 = load_23andme_txt(user1_path)
    user2 = load_23andme_txt(user2_path)

    print("Loaded User1 SNPs:", len(user1))
    print("Loaded User2 SNPs:", len(user2))

    # Plot 1
    plot_snp_overlap(user1, user2, results_dir)
    print("\n[Saved] Plot 1 outputs:")
    print("  - results/two_user_snp_overlap.png")
    print("  - results/two_user_snp_overlap.json")
    print("  - results/two_user_snp_overlap.csv")

    # Merge on shared SNPs (same as your script)
    merged = user1.merge(user2, on="SNP", suffixes=("_1", "_2"))
    print("Shared SNP count:", len(merged))

    merged["IBS"] = merged.apply(lambda r: ibs(r["genotype_1"], r["genotype_2"]), axis=1)
    merged_clean = merged.dropna(subset=["IBS"]).copy()
    merged_clean["IBS"] = merged_clean["IBS"].astype(int)

    print("Comparable SNPs after filtering:", len(merged_clean))

    # Plot 2
    plot_genotype_difference_hist(merged_clean, results_dir)
    print("\n[Saved] Plot 2 outputs:")
    print("  - results/two_user_genotype_difference_hist.png")
    print("  - results/two_user_genotype_difference_hist.json")
    print("  - results/two_user_genotype_difference_hist.csv")

    # Save per-SNP merged table (useful for your dashboard tables)
    merged_clean.to_csv(os.path.join(results_dir, "two_user_pairwise_variant_table.csv"), index=False)
    print("\n[Saved] results/two_user_pairwise_variant_table.csv")

    # Plot 3 (optional)
    out_df = plot_rare_differences_by_superpop(merged_clean, af_path, results_dir, rare_threshold=0.01)
    if out_df is not None:
        print("\n[Saved] Plot 3 outputs:")
        print("  - results/two_user_rare_differences_by_superpop.png")
        print("  - results/two_user_rare_differences_by_superpop.json")
        print("  - results/two_user_rare_differences_by_superpop.csv")
    else:
        print("\n[Skipped] Plot 3 (rare differences) — provide allele_freq_by_superpop.csv to enable it.")

    print("\nDone.")


if __name__ == "__main__":
    main()
