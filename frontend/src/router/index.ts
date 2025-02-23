import { createRouter, createWebHistory } from 'vue-router'
import ResumeList from '@/components/resume/ResumeList.vue'
import ResumeDetail from '@/components/resume/ResumeDetail.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/resumes',
      name: 'ResumeList',
      component: ResumeList
    },
    {
      path: '/resumes/:id',
      name: 'ResumeDetail',
      component: ResumeDetail
    }
  ]
})

export default router
