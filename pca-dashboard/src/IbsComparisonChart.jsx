import React from "react";
import Plot from "react-plotly.js";

export default function IbsComparisonChart() {
  const chromosomes = [
    "1","2","3","4","5","6","7","8","9","10",
    "11","12","13","14","15","16","17","18","19","20","21","22","X"
  ];

const data = [
  {
    type: "bar",
    x: chromosomes,
    y: [
      0.8377051074647561, 0.8352989739356056, 0.8259656951610654, 0.8247771288041807,
      0.8307914593032589, 0.8308483000112956, 0.8265156453715776, 0.833422842821339,
      0.8353818255087648, 0.8195895522388059, 0.8373663477771525, 0.8347744360902256,
      0.8301788955146487, 0.8287538162642243, 0.8307017543859649, 0.8396967235310046,
      0.8259874069834001, 0.8329044708909618, 0.8280431937172775, 0.8245989304812834,
      0.8315051797684339, 0.8171310017783047, 0.8711340206185567
    ],
    name: "Per-Chromosome IBS",
    marker: { color: "#4C72B0" },
    hovertemplate: '%{x}: %{y:.2%}<extra></extra>' 
  }
];


const layout = {
  title: {
    text: "Per-Chromosome IBS Between Two Users",
    font: { size: 18, color: "#000b3d" }
  },
  xaxis: {
    title: { text: "Chromosome", font: { size: 14, color: "#000b3d" } },
    type: "category", 
    showgrid: true,
    zeroline: false,
    tickmode: "array",
    tickvals: chromosomes,
    ticktext: chromosomes,
    tickangle: -45
  },
  yaxis: {
    title: { text: "Average IBS (0–1)", font: { size: 14, color: "#000b3d" } },
    range: [0, 1],
    showgrid: true,
    zeroline: false
  },
  height: 450,
  paper_bgcolor: "rgba(255,255,255,1)",
  plot_bgcolor: "rgba(255,255,255,1)"
};


  return (
    <div style={{ width: "100%", maxWidth: "900px", margin: "0 auto", padding: "20px" }}>
      <Plot 
        data={data} 
        layout={layout} 
        style={{ width: "100%" }} 
        useResizeHandler={true} 
        config={{ responsive: true }} 
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
        The graph shows how similar your DNA is to another user, chromosome by 
        chromosome using IBS calculations between two users 23andMe text files. Humans 
        naturally share 80-85% of their genetic variants, even when unrelated, which is what this 
        graph is showing. Chromosome X is often appears slightly more similar since there are 
        fewer SNPs on chromosome X. We obtained this graph by loading the users’ raw data files 
        to find all SNPs that both users share by merging their SNPs. We then computed iBS for 
        each shared SNP and, in the meantime, also removed invalid or missing genotype entries. 
        We then normalise IBS to 0(no similarity) - 1(perfect similarity) scale, a group of SNPs 
        by chromosome, and compute the average IBS per chromosome
        </p>
       <div style={{ textAlign: "left", marginTop: "20px", lineHeight: "1.6", color: "#000b3d" }}>
            <p>
                <strong>Taller bars:</strong> Greater difference between the two individuals on that chromosome, 
                indicating fewer shared alleles or more rare variants.
            </p>
            <p>
                <strong>Shorter bars:</strong> Smaller difference, indicating more shared alleles or fewer rare variants.
            </p>
            <p>
                This analysis helps reveal subtle genetic similarities or differences across chromosomes, 
                complementing broader comparisons such as overall similarity percentages.
            </p>
            </div>
      </div>
    </div>
  );
}
