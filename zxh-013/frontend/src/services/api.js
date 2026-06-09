const BASE = '/api'

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || res.statusText)
  }
  return res.json()
}

function qs(params) {
  return new URLSearchParams(params).toString()
}

export const api = {
  getMarkers(bounds, category) {
    const p = { south: bounds.south, north: bounds.north, east: bounds.east, west: bounds.west }
    if (category) p.category = category
    return request(`/markers?${qs(p)}`)
  },

  createMarker(data) {
    return request('/markers', { method: 'POST', body: JSON.stringify(data) })
  },

  getHeatmap(bounds, category) {
    const p = { south: bounds.south, north: bounds.north, east: bounds.east, west: bounds.west }
    if (category) p.category = category
    return request(`/heatmap?${qs(p)}`)
  },

  vote(markerId) {
    return request('/votes', { method: 'POST', body: JSON.stringify({ marker_id: markerId }) })
  },

  unvote(markerId) {
    return request(`/votes/${markerId}`, { method: 'DELETE' })
  },

  checkVote(markerId) {
    return request(`/votes/check/${markerId}`)
  },

  optimizeRoute(start, end) {
    return request('/route/optimize', {
      method: 'POST',
      body: JSON.stringify({ start_lat: start.lat, start_lng: start.lng, end_lat: end.lat, end_lng: end.lng }),
    })
  },

  getLeaderboard() {
    return request('/leaderboard')
  },

  getSubscriptions() {
    return request('/subscriptions')
  },

  createSubscription(data) {
    return request('/subscriptions', { method: 'POST', body: JSON.stringify(data) })
  },

  deleteSubscription(id) {
    return request(`/subscriptions/${id}`, { method: 'DELETE' })
  },

  getNotifications(sinceId = 0) {
    return request(`/subscriptions/notifications?since_id=${sinceId}`)
  },
}
