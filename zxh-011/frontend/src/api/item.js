import api from './index'

export function createItem(data) { return api.post('/items', data) }
export function listItems(params) { return api.get('/items', { params }) }
export function getItem(id) { return api.get(`/items/${id}`) }
export function updateItem(id, data) { return api.put(`/items/${id}`, data) }
export function deleteItem(id) { return api.delete(`/items/${id}`) }
