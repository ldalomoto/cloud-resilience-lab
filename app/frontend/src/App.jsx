import React, { useState } from "react";
import { sendResilienceQuery } from "./api/resilienceClient.js";
import { StatusPanel } from "./components/StatusPanel.jsx";

export default function App() {
  const [mode, setMode] = useState("normal");
  const [payload, setPayload] = useState("test-01");
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const data = await sendResilienceQuery(mode, payload);
      setResult(data);
    } catch (err) {
      setError(err.message || "Unexpected error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ fontFamily: "sans-serif", maxWidth: 520, margin: "2rem auto" }}>
      <h1>Cloud Resilience Simulator</h1>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "0.75rem" }}>
          <label htmlFor="mode-select">Mode: </label>
          <select id="mode-select" value={mode} onChange={(e) => setMode(e.target.value)}>
            <option value="normal">normal</option>
            <option value="lento">lento (timeout / retry)</option>
            <option value="caido">caido (retry / circuit breaker)</option>
          </select>
        </div>
        <div style={{ marginBottom: "0.75rem" }}>
          <label htmlFor="payload-input">Payload: </label>
          <input
            id="payload-input"
            type="text"
            value={payload}
            onChange={(e) => setPayload(e.target.value)}
          />
        </div>
        <button type="submit" disabled={loading}>
          Send Query
        </button>
      </form>
      <hr style={{ margin: "1.5rem 0" }} />
      <StatusPanel result={result} error={error} loading={loading} />
    </main>
  );
}
