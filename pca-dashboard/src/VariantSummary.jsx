import Plot from "react-plotly.js";

export function VariantSummary({ data }) {
  const yesCount = data.filter(d => d.user_has_variant === "YES").length;
  const noCount = data.length - yesCount;

  return (
    <Plot
      data={[
        {
          type: "bar",
          x: ["Present", "Absent"],
          y: [yesCount, noCount]
        }
      ]}
      layout={{
        title: "Variant Presence Summary",
        yaxis: { title: "Number of SNPs" },
        height: 300,
        paper_bgcolor: "white",
        plot_bgcolor: "white"
      }}
      config={{ responsive: true }}
    />
  );
}
