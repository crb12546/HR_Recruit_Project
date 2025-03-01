import axios from 'axios';

// 配置API基础URL
const API_BASE_URL = process.env.VUE_APP_API_BASE_URL || 'http://localhost:8000';

// 创建axios实例
const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json'
  },
  timeout: 10000 // 请求超时时间
});

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 在发送请求之前做些什么
    console.log('API请求:', config.url, config.method, config.data);
    return config;
  },
  error => {
    // 对请求错误做些什么
    console.error('API请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  response => {
    // 对响应数据做点什么
    console.log('API响应:', response.status, response.data);
    return response;
  },
  error => {
    // 对响应错误做点什么
    console.error('API响应错误:', error.response || error.message);
    return Promise.reject(error);
  }
);

// API方法
export default {
  // 简历相关API
  resumes: {
    getAll: () => api.get('/resumes'),
    getById: (id) => api.get(`/resumes/${id}`),
    create: (data) => api.post('/resumes', data),
    update: (id, data) => api.put(`/resumes/${id}`, data),
    delete: (id) => api.delete(`/resumes/${id}`),
    upload: (formData) => api.post('/resumes/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }),
    match: (resumeId, jobId) => api.get(`/resumes/${resumeId}/match/${jobId}`)
  },
  
  // 职位相关API
  jobs: {
    getAll: () => api.get('/jobs'),
    getById: (id) => api.get(`/jobs/${id}`),
    create: (data) => api.post('/jobs', data),
    update: (id, data) => api.put(`/jobs/${id}`, data),
    delete: (id) => api.delete(`/jobs/${id}`)
  },
  
  // 面试相关API
  interviews: {
    getAll: () => api.get('/interviews'),
    getById: (id) => api.get(`/interviews/${id}`),
    create: (data) => api.post('/interviews', data),
    update: (id, data) => api.put(`/interviews/${id}`, data),
    delete: (id) => api.delete(`/interviews/${id}`),
    schedule: (data) => api.post('/interviews', data),
    feedback: (id, data) => api.post(`/interviews/${id}/feedback`, data),
    questions: (id) => api.post(`/interviews/${id}/questions`)
  },
  
  // 入职相关API
  onboardings: {
    getAll: () => api.get('/onboardings'),
    getById: (id) => api.get(`/onboardings/${id}`),
    create: (data) => api.post('/onboardings', data),
    update: (id, data) => api.put(`/onboardings/${id}`, data),
    delete: (id) => api.delete(`/onboardings/${id}`)
  }
};
