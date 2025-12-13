import TraitCard from "./TraitCard";
import { useState } from "react";

const PAGE_SIZE = 4;

export default function TraitCardGrid({ data, onTraitClick }) {
  const [page, setPage] = useState(0);
  const start = page * PAGE_SIZE;
  const pageData = data.slice(start, start + PAGE_SIZE);

  return (
    <>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))",
          gap: "20px",
          marginTop: "20px",
        }}
      >
        {pageData.map((trait) => (
          <TraitCard
            key={trait.rsid}
            trait={trait}
            onClick={() => onTraitClick(trait)}
          />
        ))}
      </div>

<div style={{ marginTop: "20px", textAlign: "center", display: "flex", justifyContent: "center", gap: "20px", alignItems: "center" }}>
  <button
    onClick={() => setPage((p) => Math.max(p - 1, 0))}
    disabled={page === 0}
    style={{
      padding: "8px 16px",
      borderRadius: "8px",
      border: "none",
      background: page === 0 ? "#ccc" : "#1e88e5",
      color: "#fff",
      cursor: page === 0 ? "not-allowed" : "pointer",
      boxShadow: "0 2px 5px rgba(0,0,0,0.15)",
      fontWeight: "500",
      transition: "background 0.2s, transform 0.1s",
    }}
    onMouseEnter={(e) => (e.currentTarget.style.transform = "scale(1.05)")}
    onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1)")}
  >
    Prev
  </button>

  <span style={{ fontWeight: "500", color: "#333" }}>
    Page {page + 1} of {Math.ceil(data.length / PAGE_SIZE)}
  </span>

  <button
    onClick={() =>
      setPage((p) =>
        p + 1 < Math.ceil(data.length / PAGE_SIZE) ? p + 1 : p
      )
    }
    disabled={page + 1 >= Math.ceil(data.length / PAGE_SIZE)}
    style={{
      padding: "8px 16px",
      borderRadius: "8px",
      border: "none",
      background: page + 1 >= Math.ceil(data.length / PAGE_SIZE) ? "#ccc" : "#1e88e5",
      color: "#fff",
      cursor: page + 1 >= Math.ceil(data.length / PAGE_SIZE) ? "not-allowed" : "pointer",
      boxShadow: "0 2px 5px rgba(0,0,0,0.15)",
      fontWeight: "500",
      transition: "background 0.2s, transform 0.1s",
    }}
    onMouseEnter={(e) => (e.currentTarget.style.transform = "scale(1.05)")}
    onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1)")}
  >
    Next
  </button>
</div>

    </>
  );
}
