/**
 * API响应处理工具
 * 提供统一的API响应处理方法
 */

import { ElMessage } from 'element-plus';

/**
 * 处理API响应成功
 * @param {Object} response - API响应对象
 * @param {String} successMessage - 成功消息
 * @returns {Object} 处理后的数据
 */
export const handleSuccess = (response, successMessage = null) => {
  if (successMessage) {
    ElMessage.success(successMessage);
  }
  return response.data;
};

/**
 * 处理API响应错误
 * @param {Error} error - 错误对象
 * @param {String} defaultMessage - 默认错误消息
 * @throws {Error} 抛出处理后的错误
 */
export const handleError = (error, defaultMessage = '操作失败') => {
  console.error('API错误:', error);
  
  // 提取错误消息
  let errorMessage = defaultMessage;
  
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
        errorMessage = '服务器内部错误';
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
  
  // 抛出错误以便调用者处理
  throw new Error(errorMessage);
};

/**
 * 处理表单提交
 * @param {Function} apiCall - API调用函数
 * @param {Object} formData - 表单数据
 * @param {String} successMessage - 成功消息
 * @param {String} errorMessage - 错误消息
 * @returns {Promise} 处理结果
 */
export const handleFormSubmit = async (apiCall, formData, successMessage = '操作成功', errorMessage = '操作失败') => {
  try {
    const response = await apiCall(formData);
    return handleSuccess(response, successMessage);
  } catch (error) {
    handleError(error, errorMessage);
  }
};

/**
 * 处理数据加载
 * @param {Function} apiCall - API调用函数
 * @param {String} errorMessage - 错误消息
 * @returns {Promise} 处理结果
 */
export const handleDataLoad = async (apiCall, errorMessage = '加载数据失败') => {
  try {
    const response = await apiCall();
    return handleSuccess(response);
  } catch (error) {
    handleError(error, errorMessage);
    return null;
  }
};
