import { createRouter, createWebHistory } from 'vue-router'
import JobList from '../components/job/JobList.vue'
import JobDetail from '../components/job/JobDetail.vue'
import InterviewList from '../components/interview/InterviewList.vue'
import InterviewSchedule from '../components/interview/InterviewSchedule.vue'
import InterviewFeedback from '../components/interview/InterviewFeedback.vue'

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
  },
  {
    path: '/interviews',
    name: 'InterviewList',
    component: InterviewList
  },
  {
    path: '/interviews/new',
    name: 'InterviewSchedule',
    component: InterviewSchedule
  },
  {
    path: '/interviews/:id',
    name: 'InterviewDetail',
    component: InterviewFeedback
  },
  {
    path: '/interviews/:id/feedback',
    name: 'InterviewFeedback',
    component: InterviewFeedback
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
