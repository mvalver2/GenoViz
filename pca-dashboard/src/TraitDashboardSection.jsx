import { useEffect, useState } from "react";
import TraitCardGrid from "./TraitCardGrid";

export default function TraitDashboardSection() {
  const [traits, setTraits] = useState([]);
  const [selectedTrait, setSelectedTrait] = useState(null);

  useEffect(() => {
    fetch("/results/user_trait_variants.json")
      .then((res) => res.json())
      .then(setTraits);
  }, []);

  return (
    <div style={{ maxWidth: "1100px", margin: "0 auto" }}>
      <TraitCardGrid data={traits} onTraitClick={setSelectedTrait} />

      {selectedTrait && (
        <div
          style={{
            marginTop: "20px",
            padding: "16px",
            borderRadius: "12px",
            background: "#fff", 
            boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
          }}
        >
          <h4 style={{ marginBottom: "10px" }}>
            Explanation for {selectedTrait.gene}:
          </h4>
          <p style={{ fontSize: "0.95rem", marginBottom: "15px" }}>
            {selectedTrait.description}
          </p>
          <button
            onClick={() => setSelectedTrait(null)}
            style={{
              padding: "8px 16px",
              borderRadius: "8px",
              border: "none",
              background: "#1e88e5",
              color: "#fff",
              cursor: "pointer",
              boxShadow: "0 2px 5px rgba(0,0,0,0.15)",
              fontWeight: "500",
              transition: "background 0.2s, transform 0.1s",
              marginTop: "10px",
            }}
            onMouseEnter={(e) =>
              (e.currentTarget.style.transform = "scale(1.05)")
            }
            onMouseLeave={(e) =>
              (e.currentTarget.style.transform = "scale(1)")
            }
          >
            Close
          </button>
        </div>
      )}

      <p style={{ marginTop: "25px", fontSize: "0.9rem" }}>
        Genetic associations are based on population studies and do not determine
        individual outcomes.
      </p>
    </div>
  );
}
