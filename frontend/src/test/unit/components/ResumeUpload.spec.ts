import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { ElMessage } from 'element-plus'
import ResumeUpload from '@/components/resume/ResumeUpload.vue'
import { useResumeStore } from '@/store/resume'

describe('简历上传组件', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  const mountUpload = () => {
    return mount(ResumeUpload, {
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
  }

  it('应该在上传前验证文件类型', () => {
    const wrapper = mountUpload()
    const invalidFile = new File(['test'], 'test.exe', { type: 'application/x-msdownload' })
    
    // 使用组件的验证方法
    const result = wrapper.vm.handleBeforeUpload(invalidFile)
    
    expect(result).toBe(false)
    expect(ElMessage.error).toHaveBeenCalledWith('不支持的文件格式')
  })

  it('应该正确处理上传成功', () => {
    const wrapper = mountUpload()
    const mockResume = {
      id: 1,
      candidate_name: '张三',
      file_type: 'pdf',
      talent_portrait: '优秀的开发者',
      tags: [{ id: 1, name: 'Python' }]
    }
    
    const resumeStore = useResumeStore()
    resumeStore.addResume = vi.fn()
    
    // 调用组件的成功处理方法
    wrapper.vm.handleSuccess(mockResume)
    
    expect(ElMessage.success).toHaveBeenCalledWith('简历上传成功')
    expect(resumeStore.addResume).toHaveBeenCalledWith(mockResume)
  })

  it('应该正确处理上传失败', () => {
    const wrapper = mountUpload()
    const error = new Error('上传失败')
    
    // 调用组件的错误处理方法
    wrapper.vm.handleError(error)
    
    expect(ElMessage.error).toHaveBeenCalledWith('上传失败: 上传失败')
  })
})
