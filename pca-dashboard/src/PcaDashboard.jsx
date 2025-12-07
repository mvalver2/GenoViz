import React, { useEffect, useState } from "react";
import Plot from "react-plotly.js";

export default function PcaDashboard() {
  const [data, setData] = useState([]);
  const [selectedPoint, setSelectedPoint] = useState(null);
  const [clusterSummary, setClusterSummary] = useState(null);

  // Population filters
  const [popFilters, setPopFilters] = useState({});

  useEffect(() => {
    fetch("/results/pca_points.json")
      .then(res => res.json())
      .then(json => {
        setData(json);

        // Initialize checkboxes (all ON by default)
        const pops = [...new Set(json.map(d => d.super_pop || d.cluster))];
        const defaultFilters = {};
        pops.forEach(p => (defaultFilters[p] = true));
        setPopFilters(defaultFilters);
      });
  }, []);

  if (data.length === 0) return <p>Loading PCA...</p>;

  // Colors
  const popColors = {
    AFR: "#1f77b4",
    AMR: "#ff7f0e",
    EAS: "#2ca02c",
    EUR: "#d62728",
    SAS: "#9467bd",
    USER_CLUSTER: "#000000"
  };

  const pops = [...new Set(data.map(d => d.super_pop || d.cluster))];

  // Build traces based on filters
  const traces = pops
    .filter(pop => popFilters[pop]) // Apply checkbox filter
    .map(pop => {
      const points = data.filter(
        d => d.super_pop === pop || d.cluster === pop
      );

      if (points.length === 0) return null;

const isUser = 
  pop === "USER_CLUSTER" ||
  pop.toLowerCase().includes("user");

      return {
        x: points.map(p => p.pc1),
        y: points.map(p => p.pc2),
        mode: "markers",
        type: "scatter",
        name: isUser ? "User Sample" : pop,
        text: points.map(
          p => `${p.sample} — ${p.super_pop} (${p.cluster})`
        ),
       marker: {
          size: isUser ? 18 : 8,
          symbol: isUser ? "star" : "circle",
          color: isUser ? "#FFD700" : (popColors[pop] || "#7f7f7f"), // ⭐ bright gold
          opacity: 0.9
        }
      };
    })
    .filter(Boolean);

  function handlePointClick(event) {
    const pointIndex = event.points[0].pointIndex;
    const popName = event.points[0].data.name;

    // Find which pop the point belongs to
    const popKey = popName === "User Sample" ? "USER_CLUSTER" : popName;

    // Get the actual subset of filtered points from data
    const selectedGroup = data.filter(
      d => d.super_pop === popKey || d.cluster === popKey
    );

    const point = selectedGroup[pointIndex];
    setSelectedPoint(point);
  }

  function summarizeCluster(clusterId) {
    const items = data.filter(d => d.cluster === clusterId);
    const popCounts = {};

    items.forEach(p => {
      popCounts[p.super_pop] = (popCounts[p.super_pop] || 0) + 1;
    });

    setClusterSummary({ clusterId, popCounts, total: items.length });
  }

  const clusters = [...new Set(data.map(d => d.cluster))];

  return (
    <div style={{ display: "flex", gap: "20px" }}>

      {/* PCA PLOT */}
      <div style={{ flex: 1, borderRadius: "12px", boxShadow: "0 6px 15px rgba(0,0,0,0.3)" }}>
       <Plot
            data={traces}
            layout={{
              title: "PCA of 1000 Genomes + User",
              xaxis: { title: "PC1" },
              yaxis: { title: "PC2" },
              height: 650,
              showlegend: true,
              paper_bgcolor: "rgba(255,255,255,1)",
              plot_bgcolor: "rgba(255,255,255,1)"   
            }}
            onClick={handlePointClick}
          />
      </div>

      {/* SIDEBAR */}
      <div style={{ flex: 1, background: "#fafafa", padding: "20px", borderRadius: "12px", boxShadow: "0 6px 15px rgba(0,0,0,0.3)" }}>

        {/* Population Filters */}
        <h3>Filter Populations</h3>
        {pops.map(pop => (
          <label key={pop} style={{ display: "block", marginBottom: "5px" }}>
            <input
              type="checkbox"
              checked={popFilters[pop]}
              onChange={() =>
                setPopFilters({
                  ...popFilters,
                  [pop]: !popFilters[pop]
                })
              }
            />
            {"  "}{pop}
          </label>
        ))}

        <hr style={{ margin: "15px 0" }} />

        {/* Selected Point */}
        <h3>Selected Sample</h3>
        {selectedPoint ? (
          <div>
            <p><b>Sample:</b> {selectedPoint.sample}</p>
            <p><b>Super-pop:</b> {selectedPoint.super_pop}</p>
            <p><b>Population:</b> {selectedPoint.pop}</p>
            <p><b>Gender:</b> {selectedPoint.gender}</p>
            <p><b>Cluster:</b> {selectedPoint.cluster}</p>
          </div>
        ) : (
          <p>Click a point to see details.</p>
        )}

        {/* Cluster Summary */}
        <h3 style={{ marginTop: "20px" }}>Cluster Summary</h3>
        {clusters.map(clusterId => (
          <button
            key={clusterId}
            style={{ display: "block", margin: "5px 0" }}
            onClick={() => summarizeCluster(clusterId)}
          >
            Analyze Cluster {clusterId}
          </button>
        ))}

        {clusterSummary && (
          <div style={{ marginTop: "15px" }}>
            <h4>Cluster {clusterSummary.clusterId}</h4>
            <p><b>Total individuals:</b> {clusterSummary.total}</p>
            <ul>
              {Object.entries(clusterSummary.popCounts).map(([pop, count]) => (
                <li key={pop}>{pop}: {count}</li>
              ))}
            </ul>
          </div>
        )}

      </div>

    </div>
  );
}
