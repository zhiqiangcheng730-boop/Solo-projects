import api from './index'

export function exportPlanPdfUrl(planId) {
  return `/api/export/plan/${planId}/pdf`
}
