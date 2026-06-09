const BASE = '/api'

function buildUrl(path, params = {}) {
  const url = new URL(`${BASE}${path}`, window.location.origin)
  Object.entries(params).forEach(([k, v]) => {
    if (v !== '' && v != null) url.searchParams.set(k, v)
  })
  return url.toString()
}

export function useApi() {
  async function get(path, params = {}) {
    const res = await fetch(buildUrl(path, params))
    return res.json()
  }

  async function post(path, body) {
    const res = await fetch(buildUrl(path), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
    return res.json()
  }

  async function postForm(path, formData) {
    const res = await fetch(buildUrl(path), {
      method: 'POST',
      body: formData,
    })
    return res.json()
  }

  async function del(path) {
    const res = await fetch(buildUrl(path), { method: 'DELETE' })
    return res.json()
  }

  return { get, post, postForm, del }
}
