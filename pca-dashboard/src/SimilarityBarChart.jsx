import React from "react";
import Plot from "react-plotly.js";

export default function SimilarityBarChart() {
  const data = [
    {
      type: "bar",
      x: ["AFR", "AMR", "EAS", "EUR", "SAS"],
      y: [
        0.351320943165551,
        0.29704296074609154,
        0.31310336918533055,
        0.31524980167555605,
        0.3154479685377245,
      ],
      name: "Similarity of Individual to Super Populations",
      marker: { color: "light blue" },
    },
  ];

  const layout = {
    title: "Similarity of Individual to Super Populations",
    xaxis: { title: "Super Population" },
    yaxis: { title: "Mean |gt_user - gt_pop|" },
    height: 450,
    paper_bgcolor: "rgba(255,255,255,1)",
    plot_bgcolor: "rgba(255,255,255,1)",
    showlegend: false,
  };

  return (
    <div style={{ width: "100%", maxWidth: "800px", margin: "0 auto", padding: "20px" }}>
      <Plot data={data} layout={layout} style={{ width: "100%" }} useResizeHandler={true} config={{ responsive: true }} />

      {/* Explanation */}
      <div
        style={{
          marginTop: "20px",
          padding: "15px",
          background: "rgba(255,255,255,1)",
          borderRadius: "10px",
          lineHeight: "1.6",
          color: "#000b3d",
          textAlign: "left",
        }}
      >
        <h2 style={{ marginBottom: "10px", textAlign: "center" }}>What This Means</h2>
        <p>
         The bar plot shows the average absolute difference between the individual’s 
         allele counts and the population-average allele counts for each super-population 
         (AFR, AMR, EAS, EUR, SAS). Lower values indicate greater genetic similarity. 
         The individual shows the smallest mean difference to the Admixed American (AMR) 
         population, suggesting the highest similarity to this group based on chr22 variation, 
         while the largest difference is observed with African (AFR) populations. 
         This metric provides a simple preliminary assessment of population affinity using a 
         limited genomic subset, offering insight into which reference population is genetically 
         closest to the individual. Although coarse and chromosome-restricted, this approach can 
         guide more detailed ancestry inference (e.g., PCA, ADMIXTURE) when expanded to genome-wide data.
        </p>
       <p><strong>Big bars:</strong> Greater difference from the population, meaning fewer shared alleles or more rare variants.</p>
        <p><strong>Smaller bars:</strong> Smaller difference from the population, meaning more shared alleles or fewer rare variants.</p>
        <p>Rare variants are particularly informative for highlighting subtle genetic differences between populations.</p>
      </div>
    </div>
  );
}
