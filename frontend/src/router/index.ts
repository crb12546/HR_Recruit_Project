import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import ResumeList from '@/components/resume/ResumeList.vue'
import ResumeDetail from '@/components/resume/ResumeDetail.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/resumes'
  },
  {
    path: '/resumes',
    name: 'ResumeList',
    component: ResumeList
  },
  {
    path: '/resumes/:id',
    name: 'ResumeDetail',
    component: ResumeDetail,
    props: route => ({ id: Number(route.params.id) })
  }
] as RouteRecordRaw[]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
