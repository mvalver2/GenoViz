import pandas as pd
from cyvcf2 import VCF
import matplotlib.pyplot as plt
from collections import defaultdict

# 1. Load population info
pop_info = pd.read_csv(
    "integrated_call_samples_v3.20130502.ALL.panel",
    sep="\t"
)
# Expect columns: sample, pop, super_pop, ...
print("Population info:")
print(pop_info.head())

# Map sample -> super_pop
sample_to_super = dict(zip(pop_info["sample"], pop_info["super_pop"]))

# 2. Load the user's matched SNPs
individual = pd.read_csv("chr22_user1_matched.txt", sep="\t")
print("User SNPs (head):")
print(individual.head())

# Ensure gt_user is numeric
individual["gt_user"] = individual["gt_user"].astype(float)

# Map rsid -> gt_user
gt_user_map = dict(zip(individual["rsid"], individual["gt_user"]))
user_rsids = set(gt_user_map.keys())

print(f"Number of user SNPs: {len(user_rsids)}")

# 3. Open VCF (1000G chr22)
vcf = VCF("chr22_filtered.vcf.gz")

# Streaming aggregates
diff_sum = defaultdict(float)     # super_pop -> sum of |gt_user - gt_pop|
diff_count = defaultdict(int)     # super_pop -> number of comparisons

af_sum = defaultdict(float)       # (rsid, super_pop) -> sum of gt_pop
af_count = defaultdict(int)       # (rsid, super_pop) -> number of genotypes

total_variants = 0
matched_variants = 0

print("Scanning VCF... this may take a bit, but you should see progress updates.")

for variant in vcf:
    total_variants += 1
    if total_variants % 100000 == 0:
        print(f"Processed {total_variants} variants, matched {matched_variants} user SNPs so far...")

    rsid = variant.ID
    if rsid not in user_rsids:
        continue

    matched_variants += 1
    gt_user = gt_user_map[rsid]

    # variant.genotypes is a list of [allele1, allele2, phased_flag]
    for i, gt in enumerate(variant.genotypes):
        a1, a2 = gt[0], gt[1]

        # Skip missing genotypes
        if a1 < 0 or a2 < 0:
            continue

        sample = vcf.samples[i]
        super_pop = sample_to_super.get(sample)
        if super_pop is None:
            continue

        gt_pop = a1 + a2  # 0, 1, or 2

        # For mean genotype difference
        diff = abs(gt_user - gt_pop)
        diff_sum[super_pop] += diff
        diff_count[super_pop] += 1

        # For allele frequency (AF) per SNP per super_pop
        key = (rsid, super_pop)
        af_sum[key] += gt_pop
        af_count[key] += 1

print(f"Done scanning VCF. Total variants: {total_variants}, matched user SNPs: {matched_variants}")

# 4. Compute mean genotype difference per super_pop
mean_diff = {}
for sp in diff_sum:
    if diff_count[sp] > 0:
        mean_diff[sp] = diff_sum[sp] / diff_count[sp]

print("Mean genotype difference by super population:")
print(mean_diff)

# 5. Compute rare variant counts per super_pop (AF < 0.01)
rare_counts = defaultdict(int)

for (rsid, sp), s in af_sum.items():
    n = af_count[(rsid, sp)]
    if n == 0:
        continue
    af = s / (2.0 * n)  # genotype dosage / (2 * number of samples)
    if af < 0.01:
        rare_counts[sp] += 1

print("Rare variant counts (AF < 0.01) by super population:")
print(rare_counts)

# 6. Plot mean genotype difference
mean_diff_series = pd.Series(mean_diff).sort_index()
plt.figure()
mean_diff_series.plot(kind="bar")
plt.ylabel("Mean |gt_user - gt_pop|")
plt.title("Similarity of Individual to Super Populations")
plt.tight_layout()
plt.savefig("mean_genotype_diff_by_super_pop.png")
plt.show()

# 7. Plot rare variant counts
rare_counts_series = pd.Series(rare_counts).sort_index()
plt.figure()
rare_counts_series.plot(kind="bar")
plt.ylabel("Number of rare SNPs (AF < 0.01)")
plt.title("Rare variants per Super Population")
plt.tight_layout()
plt.savefig("rare_variant_counts_by_super_pop.png")
plt.show()
