import pandas as pd
import numpy as np
import allel
import matplotlib.pyplot as plt
import json

# 1. Load population info
pop_info = pd.read_csv(
    "integrated_call_samples_v3.20130502.ALL.panel",
    sep="\t"
)
print("Population info:")
print(pop_info.head())

# 2. Load user's matched SNPs (with gt_user)
individual = pd.read_csv("chr22_user1_matched.txt", sep="\t")
print("User SNPs (head):")
print(individual.head())

individual["gt_user"] = individual["gt_user"].astype(float)
user_gt_map = dict(zip(individual["rsid"], individual["gt_user"]))
user_rsids = set(user_gt_map.keys())
print(f"Number of user SNPs: {len(user_rsids)}")

# 3. Load subset VCF with scikit-allel
vcf_file = "chr22_subset.vcf.gz"
callset = allel.read_vcf(
    vcf_file,
    fields=["variants/ID", "calldata/GT", "samples"]
)

rsids = np.array(callset["variants/ID"])
samples = np.array(callset["samples"])
gt = allel.GenotypeArray(callset["calldata/GT"]).to_n_alt()  # (n_variants, n_samples)

print(f"Subset VCF: {gt.shape[0]} variants, {gt.shape[1]} samples")

# 4. Keep only variants that are in the user set (by rsid)
mask_match = np.isin(rsids, list(user_rsids))
rsids_match = rsids[mask_match]
gt_match = gt[mask_match, :]  # (n_match_variants, n_samples)
print(f"Matched variants between user and VCF: {gt_match.shape[0]}")

# Build vector of user genotypes in the same order as rsids_match
user_gt_vec = np.array([user_gt_map[r] for r in rsids_match])  # (n_match_variants,)

# 5. Filter population panel to samples present in VCF
pop_info = pop_info[pop_info["sample"].isin(samples)]
print(f"Samples in panel & VCF: {len(pop_info)}")

# Map sample -> index in VCF sample list
sample_to_idx = {s: i for i, s in enumerate(samples)}

# Group sample indices by super population
super_pop_to_indices = {}
for sp, group in pop_info.groupby("super_pop"):
    idxs = [sample_to_idx[s] for s in group["sample"] if s in sample_to_idx]
    if idxs:
        super_pop_to_indices[sp] = np.array(idxs, dtype=int)

print("Super populations used:", list(super_pop_to_indices.keys()))

# 6. Compute mean genotype difference and rare variant counts per super_pop
mean_diff = {}
rare_counts = {}

for sp, idxs in super_pop_to_indices.items():
    # Extract genotypes for this super_pop: shape (n_variants, n_samples_in_sp)
    gt_sp = gt_match[:, idxs]

    # Mask missing (-1) if any; allel.to_n_alt() usually gives 0,1,2 or 0 for missing,
    # but we can be safe by treating negative values as missing.
    gt_sp = gt_sp.astype(float)
    gt_sp[gt_sp < 0] = np.nan

    # --- Mean genotype difference ---
    # Broadcast user_gt_vec (n_variants,) against gt_sp (n_variants, n_samples_in_sp)
    diff = np.abs(gt_sp - user_gt_vec[:, None])  # (n_variants, n_samples_in_sp)
    mean_diff[sp] = np.nanmean(diff)

    # --- Rare variant counts ---
    # Allele frequency per variant in this super_pop
    # dosage 0/1/2 -> AF = mean(dosage) / 2
    af = np.nanmean(gt_sp, axis=1) / 2.0  # (n_variants,)
    rare_counts[sp] = int(np.sum(af < 0.01))

print("Mean genotype difference by super population:")
print(mean_diff)
print("Rare variant counts (AF < 0.01) by super population:")
print(rare_counts)

# 7. Create JSON data for Plotly chart
json_data = {
    "data": [
        {
            "type": "bar",
            "x": list(rare_counts.keys()),  # Super populations
            "y": list(rare_counts.values()),  # Rare variant counts
            "name": "Rare variants per Super Population",
            "marker": {
                "color": "blue"
            }
        }
    ],
    "layout": {
        "title": "Rare variants per Super Population",
        "xaxis": {
            "title": "Super Population"
        },
        "yaxis": {
            "title": "Number of rare SNPs (AF < 0.01)"
        }
    }
}

# 8. Write the JSON data to a file
with open('rare_variant_counts_by_super_pop_allel.json', 'w') as json_file:
    json.dump(json_data, json_file)

print("JSON file created successfully: rare_variant_counts_by_super_pop_allel.json")

# Create JSON data for Similarity of Individual to Super Populations chart
similarity_json_data = {
    "data": [
        {
            "type": "bar",
            "x": list(mean_diff.keys()),  # Super populations (from the mean_diff dictionary)
            "y": list(mean_diff.values()),  # Mean genotype differences
            "name": "Similarity of Individual to Super Populations",
            "marker": {
                "color": "blue"
            }
        }
    ],
    "layout": {
        "title": "Similarity of Individual to Super Populations",
        "xaxis": {
            "title": "Super Population"
        },
        "yaxis": {
            "title": "Mean |gt_user - gt_pop|"
        }
    }
}

# Write the JSON data to a file for Similarity chart
with open('similarity_of_individual_to_super_pop.json', 'w') as json_file:
    json.dump(similarity_json_data, json_file)

print("JSON file created successfully: similarity_of_individual_to_super_pop.json")

# 7. Plot mean genotype difference
mean_diff_series = pd.Series(mean_diff).sort_index()
plt.figure()
mean_diff_series.plot(kind="bar")
plt.ylabel("Mean |gt_user - gt_pop|")
plt.title("Similarity of Individual to Super Populations")
plt.tight_layout()
plt.savefig("mean_genotype_diff_by_super_pop_allel.png")
plt.show()

# 8. Plot rare variant counts
rare_counts_series = pd.Series(rare_counts).sort_index()
plt.figure()
rare_counts_series.plot(kind="bar")
plt.ylabel("Number of rare SNPs (AF < 0.01)")
plt.title("Rare variants per Super Population")
plt.tight_layout()
plt.savefig("rare_variant_counts_by_super_pop_allel.png")
plt.show()
