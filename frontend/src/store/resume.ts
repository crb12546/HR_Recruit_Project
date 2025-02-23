import { defineStore } from 'pinia'
import { request } from '@/utils/request'
import type { Resume } from '@/types'
import type { APIResponse } from '@/types/api'

export const useResumeStore = defineStore('resume', {
  state: () => ({
    resumes: [] as Resume[],
    loading: false,
    error: null as string | null
  }),

  actions: {
    async getResumeById(id: number): Promise<Resume> {
      try {
        const response = await request.get<APIResponse<Resume>>(`/api/v1/resumes/${id}`)
        return response.data.data
      } catch (error) {
        throw new Error('获取简历详情失败')
      }
    },

    async removeTagFromResume(resumeId: number, tagId: number): Promise<Resume> {
      try {
        const response = await request.delete<APIResponse<Resume>>(`/api/v1/resumes/${resumeId}/tags/${tagId}`)
        return response.data.data
      } catch (error) {
        throw new Error('移除标签失败')
      }
    },

    async uploadResume(file: File): Promise<Resume> {
      try {
        const formData = new FormData()
        formData.append('file', file)
        const response = await request.post<APIResponse<Resume>>('/api/v1/resumes/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })
        return response.data.data
      } catch (error) {
        throw new Error('上传简历失败')
      }
    }
  }
})
