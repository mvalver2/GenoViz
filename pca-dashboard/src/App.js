import React from "react";
import NavBar from "./NavBar";
import PcaPage from "./PcaPage";

function App() {
  return (
    <div style={{ display: "flex" }}>
      <NavBar />

      {/* Main content with left margin equal to sidebar width */}
      <div style={{ marginLeft: "150px", flex: 1, width: "100%" }}>
        <PcaPage />
      </div>
    </div>
  );
}

export default App;
