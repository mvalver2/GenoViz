export default function TraitCard({ trait, onClick }) {
  const hasVariant = trait.user_has_variant === "YES";

  return (
    <div
      onClick={onClick} 
      style={{
        cursor: "pointer", 
        borderRadius: "12px",
        padding: "16px",
        background: hasVariant ? "#e8f4ff" : "#f5f5f5",
        border: hasVariant ? "2px solid #1e88e5" : "1px solid #ccc",
        boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
        transition: "transform 0.1s",
      }}
      onMouseEnter={(e) => (e.currentTarget.style.transform = "scale(1.02)")}
      onMouseLeave={(e) => (e.currentTarget.style.transform = "scale(1)")}
    >
      <h3 style={{ marginBottom: "5px" }}>
        {trait.gene} ({trait.rsid})
      </h3>

      <p style={{ fontSize: "0.95rem", marginBottom: "10px" }}>
        {trait.trait}
      </p>

      <strong style={{ color: hasVariant ? "#1e88e5" : "#777" }}>
        Variant present: {trait.user_has_variant}
      </strong>
    </div>
  );
}
