import axios from 'axios'

const api = axios.create({ baseURL: '/api' })

export const auth = {
  register: (data) => api.post('/users/register', data),
  login: (data) => api.post('/users/login', data),
  getUser: (id) => api.get(`/users/${id}`),
}

export const skills = {
  create: (data, userId) => api.post(`/skills/?user_id=${userId}`, data),
  list: (params) => api.get('/skills/', { params }),
  search: (filters) => api.post('/skills/search', filters),
  getById: (id) => api.get(`/skills/${id}`),
  deactivate: (id, userId) => api.delete(`/skills/${id}?user_id=${userId}`),
  setUrgent: (id, userId, reason, deadline) =>
    api.put(`/skills/${id}/urgent`, null, { params: { user_id: userId, reason, deadline } }),
}

export const transactions = {
  create: (data, fromUserId) => api.post('/transactions/', data, { params: { from_user_id: fromUserId } }),
  list: (userId) => api.get('/transactions/', { params: { user_id: userId } }),
  getById: (id) => api.get(`/transactions/${id}`),
  accept: (id, userId) => api.put(`/transactions/${id}/accept`, null, { params: { user_id: userId } }),
  complete: (id, userId) => api.put(`/transactions/${id}/complete`, null, { params: { user_id: userId } }),
  cancel: (id, userId) => api.put(`/transactions/${id}/cancel`, null, { params: { user_id: userId } }),
}

export const matching = {
  matchSkill: (skillId, limit) => api.get(`/matching/skill/${skillId}`, { params: { limit } }),
  recommendations: (userId, limit) => api.get(`/matching/recommendations/${userId}`, { params: { limit } }),
}

export const reviews = {
  create: (data, reviewerId) => api.post('/reviews/', data, { params: { reviewer_id: reviewerId } }),
  getUserReviews: (userId) => api.get(`/reviews/user/${userId}`),
}

export const locationApi = {
  nearby: (lat, lon, radiusKm, limit) =>
    api.get('/location/nearby', { params: { lat, lon, radius_km: radiusKm, limit } }),
  citySkills: (city) => api.get(`/location/city/${city}`),
}

export const urgent = {
  list: (city) => api.get('/urgent/', { params: { city } }),
  mark: (id, userId, reason) => api.put(`/urgent/${id}/mark`, null, { params: { user_id: userId, reason } }),
  unmark: (id, userId) => api.put(`/urgent/${id}/unmark`, null, { params: { user_id: userId } }),
}

export const ranking = {
  topHelpers: (limit) => api.get('/ranking/helpers', { params: { limit } }),
  highestCredit: (limit) => api.get('/ranking/credit', { params: { limit } }),
}

export default api
