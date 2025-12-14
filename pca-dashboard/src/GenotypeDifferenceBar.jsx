import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";

export default function GenotypeDifferenceBar() {
  const [plotData, setPlotData] = useState(null);

  useEffect(() => {
    fetch("/results/two_user_genotype_difference_hist.json")
      .then((res) => res.json())
      .then((json) => setPlotData(json));
  }, []);

  if (!plotData) return <p>Loading genotype comparison…</p>;

  return (
    <div style={{ width: "100%", maxWidth: "900px", margin: "0 auto", padding: "20px" }}>
    <Plot
      data={plotData.data}
      layout={{
        ...plotData.layout,
        autosize: true,
        margin: { t: 60, l: 60, r: 20, b: 80 },
        paper_bgcolor: "rgba(255,255,255,255)",
        plot_bgcolor: "rgba(0,0,0,0)",
        font: { color: "#000b3d" }
      }}
      config={{ responsive: true }}
      style={{ width: "100%", height: "100%" }}
    />

    <div
        style={{
          marginTop: "25px",
          padding: "20px",
          background: "rgba(255,255,255,1)",
          borderRadius: "10px",
          lineHeight: "1.6",
          color: "#000b3d",
        }}
      >
        <h2>What This Means</h2>
        <p>
          This chart summarizes how similar two individuals are at the SNP level by counting how 
          often their genotypes are identical, partially shared, or completely different across 
          chromosome 22. Most SNPs fall into the Δ = 0 category, indicating identical genotypes, 
          which is expected given that unrelated humans typically share a large proportion of common 
          genetic variation. Smaller counts in the Δ = 1 and Δ = 2 categories reflect sites where one 
          or both alleles differ between individuals, capturing fine-scale genetic differences.
        </p>
        <h2>Why This Is Important</h2>
        <p>
         By reducing millions of genotype comparisons into a simple, interpretable distribution, 
         this visualization provides an intuitive measure of genetic similarity between two individuals. 
         Unlike a single overall similarity percentage, the histogram reveals how differences are 
         distributed;whether variation is driven by many small differences or fewer large ones. 
         This approach complements broader analyses such as PCA by offering a direct, SNP-level 
         comparison that is easy to interpret and useful for validating relatedness, exploring 
         individual variation, and contextualizing personal genomic data within population genetics.
        </p>
      </div>
    </div>
  );
}
