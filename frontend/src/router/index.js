import { createRouter, createWebHistory } from 'vue-router'
import JobList from '../components/job/JobList.vue'
import JobDetail from '../components/job/JobDetail.vue'
import InterviewList from '../components/interview/InterviewList.vue'
import InterviewSchedule from '../components/interview/InterviewSchedule.vue'
import InterviewFeedback from '../components/interview/InterviewFeedback.vue'
import OnboardingList from '../components/onboarding/OnboardingList.vue'
import OnboardingForm from '../components/onboarding/OnboardingForm.vue'
import OnboardingDetail from '../components/onboarding/OnboardingDetail.vue'

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
  },
  {
    path: '/onboardings',
    name: 'OnboardingList',
    component: OnboardingList
  },
  {
    path: '/onboardings/new',
    name: 'OnboardingCreate',
    component: OnboardingForm
  },
  {
    path: '/onboardings/:id',
    name: 'OnboardingDetail',
    component: OnboardingDetail
  },
  {
    path: '/onboardings/:id/edit',
    name: 'OnboardingEdit',
    component: OnboardingForm
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
