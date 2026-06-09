import api from './index'

export function addStep(data) { return api.post('/progress', data) }
export function listSteps(itemId) { return api.get(`/progress/item/${itemId}`) }
export function removeStep(id) { return api.delete(`/progress/${id}`) }
