import { createRouter, createWebHistory } from 'vue-router'
import JobList from '../components/job/JobList.vue'
import JobDetail from '../components/job/JobDetail.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/jobs',
    name: 'JobList',
    component: JobList
  },
  {
    path: '/jobs/:id',
    name: 'JobDetail',
    component: JobDetail
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
