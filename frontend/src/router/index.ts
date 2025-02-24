import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ResumeView from '@/views/ResumeView.vue'
import OnboardingView from '@/views/onboarding/OnboardingView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/resumes',
      name: 'resumes',
      component: ResumeView
    },
    {
      path: '/onboarding',
      name: 'onboarding',
      component: OnboardingView
    }
  ]
})

export default router
