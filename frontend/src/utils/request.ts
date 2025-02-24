import axios, { type AxiosInstance, type AxiosResponse, type AxiosError } from 'axios'
import { ElMessage } from 'element-plus'
import type { APIResponse, ErrorResponse } from '@/types/api'

export const request: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 可以在这里添加token等认证信息
    return config
  },
  (error: AxiosError) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response: AxiosResponse<APIResponse>) => {
    return response
  },
  (error: AxiosError<ErrorResponse>) => {
    // 统一错误处理
    const message = (error.response?.data as ErrorResponse)?.detail || '请求失败，请重试'
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

export default request
