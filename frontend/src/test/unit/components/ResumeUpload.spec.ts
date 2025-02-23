import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { ElUpload, ElMessage } from 'element-plus'
import ResumeUpload from '@/components/resume/ResumeUpload.vue'

describe('ResumeUpload Component', () => {
  it('should handle single file upload successfully', async () => {
    const wrapper = mount(ResumeUpload)
    const testFile = new File(['test content'], 'test.pdf', { type: 'application/pdf' })
    
    // Mock successful upload
    const mockUpload = vi.fn().mockResolvedValue({
      data: {
        id: 1,
        talent_portrait: '具有5年Python开发经验的后端工程师'
      }
    })
    wrapper.vm.uploadResume = mockUpload
    
    // Trigger file upload
    await wrapper.findComponent(ElUpload).vm.$emit('change', { raw: testFile })
    
    expect(mockUpload).toHaveBeenCalledWith(testFile)
    expect(wrapper.emitted('upload-success')).toBeTruthy()
  })

  it('should validate file type', async () => {
    const wrapper = mount(ResumeUpload)
    const invalidFile = new File(['test'], 'test.exe', { type: 'application/x-msdownload' })
    
    const mockMessage = vi.spyOn(ElMessage, 'error')
    
    // Trigger invalid file upload
    await wrapper.findComponent(ElUpload).vm.$emit('change', { raw: invalidFile })
    
    expect(mockMessage).toHaveBeenCalledWith('只支持PDF、Word和Excel格式的文件')
  })
})
