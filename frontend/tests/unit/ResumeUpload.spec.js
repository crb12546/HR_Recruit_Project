import { mount, shallowMount } from '@vue/test-utils'
import { nextTick } from 'vue'
import ResumeUpload from '@/components/resume/ResumeUpload.vue'
import { ElMessage } from 'element-plus'

// 模拟Element Plus组件
jest.mock('element-plus', () => ({
  ElMessage: {
    success: jest.fn(),
    error: jest.fn()
  }
}))

// 模拟fetch API
global.fetch = jest.fn()

describe('ResumeUpload.vue', () => {
  let wrapper
  
  beforeEach(() => {
    // 重置所有模拟
    jest.clearAllMocks()
    
    // 模拟成功的文件上传响应
    global.fetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({
        id: 1,
        candidate_name: '张三',
        file_url: 'https://example.com/resume.pdf'
      })
    })
    
    // 挂载组件
    wrapper = shallowMount(ResumeUpload)
  })
  
  it('初始化时应该正确渲染上传组件', () => {
    expect(wrapper.find('.resume-upload').exists()).toBe(true)
    expect(wrapper.find('.upload-btn').exists()).toBe(true)
    expect(wrapper.vm.uploading).toBe(false)
    expect(wrapper.vm.fileList).toEqual([])
  })
  
  it('当文件选择改变时应该更新fileList', async () => {
    const file = new File(['dummy content'], 'resume.pdf', { type: 'application/pdf' })
    
    // 模拟文件选择事件
    await wrapper.vm.handleFileChange({
      target: {
        files: [file]
      }
    })
    
    expect(wrapper.vm.fileList.length).toBe(1)
    expect(wrapper.vm.fileList[0].name).toBe('resume.pdf')
  })
  
  it('应该成功上传简历并显示成功消息', async () => {
    const file = new File(['dummy content'], 'resume.pdf', { type: 'application/pdf' })
    
    // 设置文件
    wrapper.vm.fileList = [file]
    
    // 调用上传方法
    await wrapper.vm.uploadResume()
    
    // 验证fetch被调用
    expect(global.fetch).toHaveBeenCalledWith(
      '/api/v1/resumes/upload',
      expect.objectContaining({
        method: 'POST',
        body: expect.any(FormData)
      })
    )
    
    // 验证成功消息
    expect(ElMessage.success).toHaveBeenCalledWith('简历上传成功')
    
    // 验证上传后状态重置
    expect(wrapper.vm.uploading).toBe(false)
    expect(wrapper.vm.fileList).toEqual([])
  })
  
  it('上传失败时应该显示错误消息', async () => {
    // 模拟上传失败
    global.fetch.mockResolvedValue({
      ok: false,
      json: () => Promise.resolve({ detail: '上传失败' })
    })
    
    const file = new File(['dummy content'], 'resume.pdf', { type: 'application/pdf' })
    wrapper.vm.fileList = [file]
    
    // 调用上传方法
    await wrapper.vm.uploadResume()
    
    // 验证错误消息
    expect(ElMessage.error).toHaveBeenCalledWith('上传失败: 上传失败')
    
    // 验证上传后状态
    expect(wrapper.vm.uploading).toBe(false)
  })
  
  it('网络错误时应该显示错误消息', async () => {
    // 模拟网络错误
    global.fetch.mockRejectedValue(new Error('网络错误'))
    
    const file = new File(['dummy content'], 'resume.pdf', { type: 'application/pdf' })
    wrapper.vm.fileList = [file]
    
    // 调用上传方法
    await wrapper.vm.uploadResume()
    
    // 验证错误消息
    expect(ElMessage.error).toHaveBeenCalledWith('上传失败: 网络错误')
    
    // 验证上传后状态
    expect(wrapper.vm.uploading).toBe(false)
  })
})
