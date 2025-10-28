import React, { useState } from "react";

function Analyze() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return alert("Veuillez sélectionner un fichier");

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setResult("");

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setResult(data.result); // Déjà du HTML sécurisé côté backend
    } catch (err) {
      console.error(err);
      setResult("❌ Erreur lors de l'analyse");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        maxWidth: "700px",
        margin: "50px auto",
        fontFamily: "Arial, sans-serif",
        lineHeight: 1.6,
        padding: "20px",
        backgroundColor: "#f9f9f9",
        borderRadius: "8px",
        boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
      }}
    >
      <h2 style={{ textAlign: "center", color: "#2e6c80" }}>Analyse de CV</h2>
      <form
        onSubmit={handleSubmit}
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          marginBottom: "20px",
        }}
      >
        <input type="file" onChange={handleFileChange} />
        <button
          type="submit"
          style={{
            marginLeft: "10px",
            padding: "5px 15px",
            backgroundColor: "#2e6c80",
            color: "#fff",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          {loading ? "Analyse en cours..." : "Analyser"}
        </button>
      </form>

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h3 style={{ color: "#2e6c80" }}>Résultat :</h3>
          <div dangerouslySetInnerHTML={{ __html: result }} />
        </div>
      )}
    </div>
  );
}

export default Analyze;
