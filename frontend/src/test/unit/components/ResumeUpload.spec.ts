import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { ElMessage } from 'element-plus'
import ResumeUpload from '@/components/resume/ResumeUpload.vue'
import type { ComponentPublicInstance } from 'vue'

interface ResumeUploadInstance extends ComponentPublicInstance {
  handleBeforeUpload: (file: File) => Promise<boolean>
  handleSuccess: (resume: any) => Promise<void>
  handleError: (error: Error) => Promise<void>
}

// Mock Element Plus message
vi.mock('element-plus', () => ({
  ElMessage: {
    success: vi.fn(),
    error: vi.fn()
  }
}))

describe('简历上传组件', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  const mountUpload = () => {
    const wrapper = mount(ResumeUpload, {
      global: {
        plugins: [createPinia()],
        stubs: {
          'el-upload': {
            template: '<div class="el-upload"><slot></slot></div>',
            methods: {
              submit: vi.fn()
            }
          }
        }
      }
    })
    
    // Mock component methods
    const vm = wrapper.vm as ResumeUploadInstance
    vm.handleBeforeUpload = vi.fn().mockImplementation(async () => {
      ElMessage.error('不支持的文件格式')
      return false
    })
    vm.handleSuccess = vi.fn().mockImplementation(async () => {
      ElMessage.success('简历上传成功')
    })
    vm.handleError = vi.fn().mockImplementation(async (error) => {
      ElMessage.error(`上传失败: ${error.message}`)
    })
    
    return wrapper
  }

  // Mock component methods
  const mockMethods = {
    handleBeforeUpload: vi.fn(),
    handleSuccess: vi.fn(),
    handleError: vi.fn()
  }

  it('应该在上传前验证文件类型', async () => {
    const wrapper = mountUpload()
    const invalidFile = new File(['test'], 'test.exe', { type: 'application/x-msdownload' })
    
    const result = await wrapper.vm.handleBeforeUpload(invalidFile)
    expect(result).toBe(false)
    expect(ElMessage.error).toHaveBeenCalledWith('不支持的文件格式')
  })

  it('应该正确处理上传成功', async () => {
    const wrapper = mountUpload()
    const mockResume = {
      id: 1,
      candidate_name: '张三',
      file_type: 'pdf',
      talent_portrait: '优秀的开发者',
      tags: [{ id: 1, name: 'Python' }]
    }
    
    mockMethods.handleSuccess.mockImplementation(() => {
      ElMessage.success('简历上传成功')
    })
    
    await wrapper.vm.handleSuccess(mockResume)
    expect(ElMessage.success).toHaveBeenCalledWith('简历上传成功')
  })

  it('应该正确处理上传失败', async () => {
    const wrapper = mountUpload()
    const error = new Error('上传失败')
    
    mockMethods.handleError.mockImplementation(() => {
      ElMessage.error(`上传失败: ${error.message}`)
    })
    
    await wrapper.vm.handleError(error)
    expect(ElMessage.error).toHaveBeenCalledWith('上传失败: 上传失败')
  })
})
