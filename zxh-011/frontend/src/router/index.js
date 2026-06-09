import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'Gallery', component: () => import('../views/Gallery.vue') },
  { path: '/upload', name: 'Upload', component: () => import('../views/UploadItem.vue') },
  { path: '/detail/:id', name: 'Detail', component: () => import('../views/Detail.vue') },
  { path: '/profile', name: 'Profile', component: () => import('../views/Profile.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
