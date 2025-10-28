import React from "react";
import { Link } from "react-router-dom";

function Home() {
  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>Mosaic Hire Frontend 🚀</h1>
      <p>Bienvenue sur l'application React pour analyser les CV</p>
      <Link to="/analyze">
        <button>Analyser un CV</button>
      </Link>
    </div>
  );
}

export default Home;
