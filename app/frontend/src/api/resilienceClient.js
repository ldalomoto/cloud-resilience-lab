const DEFAULT_API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function sendResilienceQuery(mode, payload = "sample-request") {
  const response = await fetch(`${DEFAULT_API_BASE}/api/v1/consultar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ modo: mode, payload }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error ${response.status}`);
  }

  return response.json();
}
