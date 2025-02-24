import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useResumeStore = defineStore('resume', () => {
  const uploadedResumes = ref<any[]>([])
  const currentResume = ref<any>(null)

  const addResume = (resume: any) => {
    uploadedResumes.value.push(resume)
  }

  const setCurrentResume = (resume: any) => {
    currentResume.value = resume
  }

  return {
    uploadedResumes,
    currentResume,
    addResume,
    setCurrentResume
  }
})
