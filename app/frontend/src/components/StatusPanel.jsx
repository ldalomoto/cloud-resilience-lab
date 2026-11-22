import React from "react";

export function StatusPanel({ result, error, loading }) {
  if (loading) {
    return <p>Sending request...</p>;
  }

  if (error) {
    return <p>Request failed: {error}</p>;
  }

  if (!result) {
    return <p>No response yet. Trigger a query to test resilience behavior.</p>;
  }

  return (
    <div>
      <h3>Latest Response</h3>
      <ul>
        <li><strong>Status:</strong> {result.estado}</li>
        <li><strong>Attempts:</strong> {result.intentos}</li>
        <li><strong>Circuit State:</strong> {result.circuito}</li>
        <li><strong>Instance:</strong> {result.instancia}</li>
        <li><strong>Detail:</strong> {result.detalle}</li>
      </ul>
    </div>
  );
}
