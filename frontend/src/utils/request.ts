import axios from 'axios'
import { ElMessage } from 'element-plus'

export const request = axios.create({
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
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response
  },
  error => {
    // 统一错误处理
    const message = error.response?.data?.detail || '请求失败，请重试'
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

export default request
