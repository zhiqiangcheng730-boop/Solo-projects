import api from './index'

export function toggleItemLike(data) { return api.post('/likes/item/toggle', data) }
export function togglePlanLike(data) { return api.post('/likes/plan/toggle', data) }
export function getItemLikes(itemId, userId) { return api.get(`/likes/item/${itemId}`, { params: { user_id: userId } }) }
export function getPlanLikes(planId, userId) { return api.get(`/likes/plan/${planId}`, { params: { user_id: userId } }) }
