import React, { useState } from "react";
import Plot from "react-plotly.js";

export default function RareVariantToggle({ labels, values }) {
  const [view, setView] = useState("bar"); // "bar" or "pie"

  const explanation = `
  These rare variants (AF < 0.01) represent genetic differences that occur in
  less than 1% of the global population. The distribution across super-populations
  shows which ancestral groups your unique variations most closely align with.
  A higher contribution in a region suggests more shared ancestry or historical
  genetic similarity with that population.
  `;

  return (
    < div style={{ width: "100%" }}>
      
      {/* Toggle Buttons */}
      <div style={{ marginBottom: "15px" }}>
        <button
          onClick={() => setView("bar")}
          style={{
            padding: "10px 20px",
            marginRight: "10px",
            background: view === "bar" ? "#000b3d" : "#dfe8ff",
            color: view === "bar" ? "white" : "#000b3d",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer",
            fontWeight: "bold"
          }}
        >
          Bar Chart
        </button>

        <button
          onClick={() => setView("pie")}
          section id = "rarevariants"
          style={{
            padding: "10px 20px",
            background: view === "pie" ? "#000b3d" : "#dfe8ff",
            color: view === "pie" ? "white" : "#000b3d",
            border: "none",
            borderRadius: "8px",
            cursor: "pointer",
            fontWeight: "bold"
          }}
        >
          Pie Chart
        </button>
      </div>

      {/* Dynamic Chart */}
      {view === "bar" ? (
        <Plot
          data={[
            {
              type: "bar",
              x: labels,
              y: values,
              marker: { color: "#7db3ff" }
            }
          ]}
          layout={{
            title: "Rare Variants per Super Population",
            height: 450,
            paper_bgcolor: "rgba(255,255,255,1)",
            plot_bgcolor: "rgba(255,255,255,1)",
            xaxis: { title: "Super Population" },
            yaxis: { title: "Number of Rare SNPs (AF < 0.01)" }
          }}
          style={{ width: "100%" }}
        />
      ) : (
        <Plot
          data={[
            {
              type: "pie",
              labels: labels,
              values: values,
              hole: 0.45,
              textinfo: "label+percent",
              hoverinfo: "label+value+percent",
              pull: 0.03
            }
          ]}
          layout={{
            title: "Rare Variant Proportion by Super Population",
            height: 450,
            paper_bgcolor: "rgba(255,255,255,1)",
            plot_bgcolor: "rgba(255,255,255,1)"
          }}
          style={{ width: "100%" }}
        />
      )}

      {/* Explanation */}
      <div
        style={{
          marginTop: "20px",
          padding: "15px",
          background: "rgba(255,255,255,0.6)",
          borderRadius: "8px",
          textAlign: "left",
          lineHeight: "1.5",
          color: "#000b3d"
        }}
      >
        <h3 style={{ marginBottom: "8px" }}>What does this mean?</h3>
        <p>{explanation}</p>
      </div>
    </div>
  );
}
