import api from './index'

export function createPlan(data) { return api.post('/renovations', data) }
export function listPlans(itemId) { return api.get(`/renovations/item/${itemId}`) }
export function getPlan(id) { return api.get(`/renovations/${id}`) }
