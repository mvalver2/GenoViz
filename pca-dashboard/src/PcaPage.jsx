import React from "react";
import PcaDashboard from "./PcaDashboard";

export default function PcaPage() {
  return (
    <div style={{ padding: "30px", fontFamily: "Arial, sans-serif", maxWidth: "1200px", margin: "0 auto" }}>
      
      {/* HEADER */}
      <header style={{ marginBottom: "40px", textAlign: "center" }}>
        <h1 style={{ fontSize: "2.5rem", marginBottom: "10px" }}>Genoviz</h1>
        <p style={{ fontSize: "1.1rem", lineHeight: "1.6" }}>
          For this project we analyse Chromosome 22 Population and Individual Genetics. This project visualizes genetic variation across different human populations using different gene analysis techniques including, 
          Principal Component Analysis (PCA), IBS (Identical By State) Pairwise Comparison, and Super Population Comparisons. Along with this, 
          we have a tool to compare two distinct individuals' 23andMe genetic data files and give a genetic similarity score and breakdown for 
          Chromosome 22. Through our analysis it allows users to explore relationships between samples from the 1000 Genomes Project and a user-provided sample. 
          You can filter populations, identify individual samples, and analyze clusters to gain insights into population structure and diversity.
        </p>
      </header>

      {/* PCA DASHBOARD */}
      <section style={{ textAlign: "center" }}>
        <h2 style={{ fontSize: "1.8rem", marginBottom: "15px" }}>Interactive PCA Plot</h2>
        <p style={{ fontSize: "1rem", marginBottom: "20px" }}>
          Use the filters to highlight different populations. Click on points to view detailed sample information. 
          Analyze clusters to see the population composition.
        </p>
        
        <PcaDashboard />
      </section>

    </div>
  );
}

