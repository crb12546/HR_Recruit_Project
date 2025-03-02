import axios from 'axios';
import { ElMessage } from 'element-plus';

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
    
    // 提取错误消息
    let errorMessage = '操作失败';
    
    if (error.response) {
      // 服务器返回错误
      const { status, data } = error.response;
      
      // 根据状态码处理
      switch (status) {
        case 400:
          errorMessage = data.detail || '请求参数错误';
          break;
        case 401:
          errorMessage = '未授权，请重新登录';
          break;
        case 403:
          errorMessage = '没有权限执行此操作';
          break;
        case 404:
          errorMessage = data.detail || '请求的资源不存在';
          break;
        case 500:
          errorMessage = data.detail || '服务器内部错误';
          break;
        default:
          errorMessage = data.detail || `请求失败 (${status})`;
      }
    } else if (error.request) {
      // 请求发送但没有收到响应
      errorMessage = '服务器无响应，请检查网络连接';
    }
    
    // 显示错误消息
    ElMessage.error(errorMessage);
    
    return Promise.reject(error);
  }
);

// 处理API响应
const handleResponse = (promise, successMessage = null) => {
  return promise
    .then(response => {
      if (successMessage) {
        ElMessage.success(successMessage);
      }
      return response;
    })
    .catch(error => {
      // 错误已在拦截器中处理
      throw error;
    });
};

// API方法
const apiService = {
  // 简历相关API
  resumes: {
    getAll: () => handleResponse(api.get('/resumes')),
    getById: (id) => handleResponse(api.get(`/resumes/${id}`)),
    create: (data) => handleResponse(api.post('/resumes', data), '简历创建成功'),
    update: (id, data) => handleResponse(api.put(`/resumes/${id}`, data), '简历更新成功'),
    delete: (id) => handleResponse(api.delete(`/resumes/${id}`), '简历删除成功'),
    upload: (formData) => handleResponse(api.post('/resumes/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }), '简历上传成功'),
    match: (resumeId, jobId) => handleResponse(api.get(`/resumes/${resumeId}/match/${jobId}`))
  },
  
  // 职位相关API
  jobs: {
    getAll: () => handleResponse(api.get('/jobs')),
    getById: (id) => handleResponse(api.get(`/jobs/${id}`)),
    create: (data) => handleResponse(api.post('/jobs', data), '职位创建成功'),
    update: (id, data) => handleResponse(api.put(`/jobs/${id}`, data), '职位更新成功'),
    delete: (id) => handleResponse(api.delete(`/jobs/${id}`), '职位删除成功')
  },
  
  // 面试相关API
  interviews: {
    getAll: () => handleResponse(api.get('/interviews')),
    getById: (id) => handleResponse(api.get(`/interviews/${id}`)),
    create: (data) => handleResponse(api.post('/interviews', data), '面试创建成功'),
    update: (id, data) => handleResponse(api.put(`/interviews/${id}`, data), '面试更新成功'),
    delete: (id) => handleResponse(api.delete(`/interviews/${id}`), '面试删除成功'),
    schedule: (data) => handleResponse(api.post('/interviews', data), '面试安排成功'),
    feedback: (id, data) => handleResponse(api.post(`/interviews/${id}/feedback`, data), '面试反馈提交成功'),
    questions: (id) => handleResponse(api.post(`/interviews/${id}/questions`))
  },
  
  // 入职相关API
  onboardings: {
    getAll: () => handleResponse(api.get('/onboardings')),
    getById: (id) => handleResponse(api.get(`/onboardings/${id}`)),
    create: (data) => handleResponse(api.post('/onboardings', data), '入职创建成功'),
    update: (id, data) => handleResponse(api.put(`/onboardings/${id}`, data), '入职更新成功'),
    delete: (id) => handleResponse(api.delete(`/onboardings/${id}`), '入职删除成功')
  }
};

export default apiService;
