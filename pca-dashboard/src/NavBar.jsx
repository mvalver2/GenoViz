import React from "react";

export default function NavBar() {
  const tabs = ["Overview", "PCA Plot", "IBS Comparison", "Individual Comparison"];

  return (
    <div 
      style={{
        width: "180px",
        height: "100vh",
        background:  "rgba(255,255,255,0.2)", // let the body gradient show
        padding: "0px 10px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",    
        alignItems: "center",        
        gap: "40px",                 
        position: "fixed",
        top: 0,
        left: 0,
        zIndex: 1000,
        fontFamily: "Arial, sans-serif", // same as your page
        color: "#000b3d"
      }}
    >
      {tabs.map((tab, idx) => (
        <a
          key={idx}
          href={`#${tab.toLowerCase().replace(/\s/g, "")}`}
          style={{
            textDecoration: "none",
            padding: "8px 0",
            borderBottom: "2px solid rgba(0,0,0,0.2)",
            width: "100%",
            textAlign: "left",
            transition: "all 0.2s ease",
            cursor: "pointer",
            color: "#000b3d",
            fontWeight: "bold",
            fontSize: "1.2rem"
          }}
          onMouseEnter={e => {
            e.target.style.borderBottom = "2px solid #000b3d";
            e.target.style.color = "#000b3d";
          }}
          onMouseLeave={e => {
            e.target.style.borderBottom = "2px solid rgba(0,0,0,0.2)";
            e.target.style.color = "#000b3d";
          }}
        >
          {tab}
        </a>
      ))}
    </div>
  );
}

