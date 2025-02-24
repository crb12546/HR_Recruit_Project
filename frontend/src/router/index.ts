import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue')
    },
    {
      path: '/resume',
      name: 'resume',
      component: () => import('@/views/ResumeView.vue')
    }
  ]
})

export default router
