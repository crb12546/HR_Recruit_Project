import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { ElMessage } from 'element-plus'
import ResumeUpload from '@/components/resume/ResumeUpload.vue'

vi.mock('element-plus', () => ({
  ElMessage: {
    error: vi.fn(),
    success: vi.fn()
  }
}))

describe('简历上传组件', () => {
  it('应该在上传前验证文件类型', async () => {
    const wrapper = mount(ResumeUpload)
    const invalidFile = new File(['test'], 'test.exe', { type: 'application/x-msdownload' })
    
    const mockMessage = vi.spyOn(ElMessage, 'error')
    await wrapper.vm.beforeUpload(invalidFile)
    
    expect(mockMessage).toHaveBeenCalledWith('只支持PDF、Word和Excel格式的文件')
    expect(wrapper.emitted('upload-success')).toBeFalsy()
  })

  it('应该正确处理上传成功', async () => {
    const wrapper = mount(ResumeUpload)
    const mockResponse = { id: 1, status: 'success' }
    
    const mockMessage = vi.spyOn(ElMessage, 'success')
    await wrapper.vm.handleSuccess(mockResponse)
    
    expect(mockMessage).toHaveBeenCalledWith('简历上传成功')
    const emitted = wrapper.emitted('upload-success')
    expect(emitted).toBeTruthy()
    expect(emitted && emitted[0]).toEqual([mockResponse])
  })

  it('应该正确处理上传失败', async () => {
    const wrapper = mount(ResumeUpload)
    const mockMessage = vi.spyOn(ElMessage, 'error')
    
    await wrapper.vm.handleError()
    
    expect(mockMessage).toHaveBeenCalledWith('上传失败，请重试')
  })
})
