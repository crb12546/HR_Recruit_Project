import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Resume } from '@/types'
import { request } from '@/utils/request'

export const useResumeStore = defineStore('resume', () => {
  const uploadedResumes = ref<Resume[]>([])
  const currentResume = ref<Resume | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const uploadResume = async (file: File) => {
    loading.value = true
    error.value = null
    
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await request.post('/resumes/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      uploadedResumes.value.push(response.data)
      return response.data
    } catch (err: any) {
      error.value = err.message || '上传失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const fetchResumes = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await request.get('/resumes')
      uploadedResumes.value = response.data
    } catch (err: any) {
      error.value = err.message || '获取简历列表失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const parseResume = async (resumeId: number) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await request.post(`/resumes/${resumeId}/parse`)
      const index = uploadedResumes.value.findIndex(r => r.id === resumeId)
      if (index !== -1) {
        uploadedResumes.value[index] = response.data
      }
      return response.data
    } catch (err: any) {
      error.value = err.message || '解析失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    uploadedResumes,
    currentResume,
    loading,
    error,
    uploadResume,
    fetchResumes,
    parseResume
  }
})
