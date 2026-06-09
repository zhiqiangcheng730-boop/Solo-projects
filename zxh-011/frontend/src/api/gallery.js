import api from './index'

export function getFeatured(params) { return api.get('/gallery/featured', { params }) }
export function getHot(limit = 10) { return api.get('/gallery/hot', { params: { limit } }) }
export function getPlanDetail(id) { return api.get(`/gallery/plans/${id}`) }
