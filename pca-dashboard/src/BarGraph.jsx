import React from "react";
import Plot from "react-plotly.js";

export default function BareGraph() {
  const data = [
    {
      type: "bar",
      x: ["AFR", "AMR", "EAS", "EUR", "SAS"],
      y: [3246, 1940, 2988, 1311, 2610],
      marker: { color: "light blue" },
    },
  ];

  const layout = {
    xaxis: { title: "Super Population" },
    yaxis: { title: "Number of rare SNPs (AF < 0.01)" },
    height: 450,
    paper_bgcolor: "rgba(255,255,255,1)",
    plot_bgcolor: "rgba(255,255,255,1)",
  };

  return (
    <div style={{ width: "100%", maxWidth: "850px", margin: "0 auto", padding: "20px" }}>

      {/* Plotly Bar Chart */}
      <Plot
        data={data}
        layout={layout}
        style={{ width: "100%" }}
        useResizeHandler={true}
        config={{ responsive: true }}
      />

{/* Explanation */}
<div
  style={{
    marginTop: "25px",
    padding: "20px",
    background: "rgba(255,255,255,1)",
    borderRadius: "12px",
    lineHeight: "1.7",
    color: "#000b3d",
    textAlign: "left",
    maxWidth: "800px",
    marginLeft: "auto",
    marginRight: "auto",
  }}
>
        <h2 style={{ marginBottom: "15px", textAlign: "center" }}>What This Means</h2>
        <p>
          Counts of rare variants in the individual across the five 1000 Genomes super-populations. 
          A variant is defined as “rare” in a population when the ALT allele frequency (AF) 
          is below 1% in that group. For each super-population (AFR, AMR, EAS, EUR, SAS), the number 
          of the user’s chr22 SNPs meeting this criterion is shown. Higher bars indicate that more of 
          the user’s alleles are uncommon in that population. The individual shows the highest number of 
          rare alleles relative to African, East Asian, and South Asian populations, and the lowest 
          relative to Europeans. These patterns highlight population-specific allele rarity and help 
          identify which groups consider the user’s variants unusual, supporting analyses of both 
          ancestry-related variation and potentially medically relevant rare alleles.
        </p>

        <p><strong>Big bars:</strong> More of the user’s alleles are uncommon in that population</p>
        <p><strong>Smaller bars:</strong> Less of their variants are considered rare for that population</p>
        <p>Rare variants are particularly informative for detecting subtle population structure.</p>
      </div>
    </div>
  );
}
