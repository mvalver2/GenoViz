import React from "react";
import PcaDashboard from "./PcaDashboard";
import BarGraph from "./BarGraph"; // Your bar chart + explanation

export default function PcaPage() {
  return (
    <div style={{ width: "100%", minHeight: "100vh", padding: "30px 0", boxSizing: "border-box" }}>
      
      {/* Inner container */}
      <div style={{ maxWidth: "1200px", margin: "0 auto", fontFamily: "Arial, sans-serif", background: "transparent" }}>
        
        {/* HEADER */}
        <header id="overview" style={{ marginBottom: "40px", textAlign: "center", padding: "20px", background: "rgba(255,255,255,0.5)", borderRadius: "12px", boxShadow: "0 4px 15px rgba(0,0,0,0.2)" }}>
          <h1 style={{ fontSize: "2.5rem", marginBottom: "10px", color: "#000b3d" }}>Genoviz</h1>
          <p style={{ fontSize: "1.1rem", lineHeight: "1.6" }}>
            For this project we analyse Chromosome 22 Population and Individual Genetics. This project visualizes genetic variation across different human populations using different gene analysis techniques including, 
            Principal Component Analysis (PCA), IBS (Identical By State) Pairwise Comparison, and Super Population Comparisons. Along with this, 
            we have a tool to compare two distinct individuals 23andMe genetic data files and give a genetic similarity score and breakdown for 
            chromosome 22. Through our analysis it allows users to explore relationships between samples from the 1000 Genomes Project and a user-provided sample. 
            You can filter populations, identify individual samples, and analyze clusters to gain insights into population structure and diversity.
          </p>
        </header>

        {/* PCA DASHBOARD */}
        <section id="pcaplot" style={{ textAlign: "center", padding: "20px", background: "rgba(255,255,255,0.5)", borderRadius: "12px", boxShadow: "0 4px 15px rgba(0,0,0,0.2)" }}>
          <h2 style={{ fontSize: "1.8rem", marginBottom: "15px", color: "#000b3d" }}>Interactive PCA Plot</h2>
          <p style={{ fontSize: "1rem", marginBottom: "20px", color: "#000b3d" }}>
            Use the filters to highlight different populations. Click on points to view detailed sample information. 
            Analyze clusters to see the population composition.
          </p>
          <PcaDashboard />
        </section>

        {/* RARE VARIANTS BAR CHART */}
        <section
          id="rarevariants"
          style={{
            textAlign: "center",
            padding: "20px",
            marginTop: "40px",
            background: "rgba(255,255,255,0.5)",
            borderRadius: "12px",
            boxShadow: "0 4px 15px rgba(0,0,0,0.2)"
          }}
        >
          <h2 style={{ fontSize: "1.8rem", marginBottom: "15px", color: "#000b3d" }}>
            Rare Variants by Super Population
          </h2>

          <p style={{ fontSize: "1rem", marginBottom: "20px", color: "#000b3d" }}>
            Explore the distribution of your rare variants (AF &lt; 0.01) across global super-populations.
          </p>

          <BarGraph /> {/* This will display the bar chart + explanations */}
        </section>

      </div>
    </div>
  );
}
