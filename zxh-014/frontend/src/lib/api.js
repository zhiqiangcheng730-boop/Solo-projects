const BASE = "/api";

async function request(url, options = {}) {
  const res = await fetch(`${BASE}${url}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "Request failed");
  }
  return res.json();
}

export const api = {
  // Dreams
  createDream: (data) => request("/dreams", { method: "POST", body: JSON.stringify(data) }),
  listDreams: (userId, skip = 0, limit = 50) =>
    request(`/dreams?user_id=${userId}&skip=${skip}&limit=${limit}`),
  getDream: (id) => request(`/dreams/${id}`),

  // Symbols
  listSymbols: (skip = 0, limit = 200) => request(`/symbols?skip=${skip}&limit=${limit}`),
  getSymbol: (keyword) => request(`/symbols/${keyword}`),
  getExplanations: (symbolId) => request(`/symbols/${symbolId}/explanations`),
  addExplanation: (data) =>
    request("/symbols/explanations", { method: "POST", body: JSON.stringify(data) }),
  voteExplanation: (data) =>
    request("/symbols/explanations/vote", { method: "POST", body: JSON.stringify(data) }),
  getTopExplanations: (symbolId, limit = 5) =>
    request(`/symbols/${symbolId}/explanations/top?limit=${limit}`),

  // Stats
  getOverview: () => request("/stats/overview"),
  getTopKeywords: (limit = 30) => request(`/stats/keywords/top?limit=${limit}`),
  getTopExplanations: (limit = 10) => request(`/stats/explanations/top?limit=${limit}`),
  getEmotionCorrelation: () => request("/stats/emotion-correlation"),

  // Sharing
  createShare: (dreamId) => request("/shares", { method: "POST", body: JSON.stringify({ dream_id: dreamId }) }),
  listShares: (skip = 0, limit = 20) => request(`/shares?skip=${skip}&limit=${limit}`),
  getShareByToken: (token) => request(`/shares/token/${token}`),
  addComment: (shareId, data) =>
    request(`/shares/${shareId}/comments`, { method: "POST", body: JSON.stringify(data) }),
  getComments: (shareId) => request(`/shares/${shareId}/comments`),
};
