import { describe, it, expect, vi, beforeEach } from 'vitest'
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
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('文件类型验证', () => {
    it('应该允许上传PDF文件', async () => {
      const wrapper = mount(ResumeUpload)
      const pdfFile = new File(['test'], 'test.pdf', { type: 'application/pdf' })
      
      const result = await wrapper.vm.beforeUpload(pdfFile)
      expect(result).toBe(true)
    })

    it('应该允许上传Word文件', async () => {
      const wrapper = mount(ResumeUpload)
      const docxFile = new File(['test'], 'test.docx', { 
        type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' 
      })
      
      const result = await wrapper.vm.beforeUpload(docxFile)
      expect(result).toBe(true)
    })

    it('应该允许上传Excel文件', async () => {
      const wrapper = mount(ResumeUpload)
      const xlsxFile = new File(['test'], 'test.xlsx', { 
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' 
      })
      
      const result = await wrapper.vm.beforeUpload(xlsxFile)
      expect(result).toBe(true)
    })

    it('应该拒绝不支持的文件类型', async () => {
      const wrapper = mount(ResumeUpload)
      const invalidFile = new File(['test'], 'test.exe', { type: 'application/x-msdownload' })
      
      const mockMessage = vi.spyOn(ElMessage, 'error')
      const result = await wrapper.vm.beforeUpload(invalidFile)
      
      expect(result).toBe(false)
      expect(mockMessage).toHaveBeenCalledWith('只支持PDF、Word和Excel格式的文件')
    })
  })

  describe('文件大小验证', () => {
    it('应该拒绝超过100MB的文件', async () => {
      const wrapper = mount(ResumeUpload)
      const largeFile = new File(['x'.repeat(105 * 1024 * 1024)], 'large.pdf', { type: 'application/pdf' })
      
      const mockMessage = vi.spyOn(ElMessage, 'error')
      const result = await wrapper.vm.beforeUpload(largeFile)
      
      expect(result).toBe(false)
      expect(mockMessage).toHaveBeenCalledWith('文件大小不能超过100MB')
    })
  })

  describe('批量上传功能', () => {
    it('应该支持多文件选择', () => {
      const wrapper = mount(ResumeUpload)
      expect(wrapper.find('.el-upload').attributes('multiple')).toBe('true')
    })

    it('应该限制最大上传数量为10个', () => {
      const wrapper = mount(ResumeUpload)
      expect(wrapper.find('.el-upload').attributes('limit')).toBe('10')
    })

    it('应该在超出数量限制时提示', async () => {
      const wrapper = mount(ResumeUpload)
      const mockMessage = vi.spyOn(ElMessage, 'error')
      
      await wrapper.vm.handleExceed()
      expect(mockMessage).toHaveBeenCalledWith('最多只能上传10个文件')
    })
  })

  describe('上传状态处理', () => {
    it('应该显示上传进度', async () => {
      const wrapper = mount(ResumeUpload)
      const event = { percent: 50 }
      
      await wrapper.vm.handleProgress(event)
      expect(wrapper.vm.uploadProgress).toBe(50)
    })

    it('应该正确处理上传成功', async () => {
      const wrapper = mount(ResumeUpload)
      const mockResponse = { id: 1, status: 'success' }
      
      const mockMessage = vi.spyOn(ElMessage, 'success')
      await wrapper.vm.handleSuccess(mockResponse)
      
      expect(mockMessage).toHaveBeenCalledWith('简历上传成功')
      expect(wrapper.vm.uploadProgress).toBe(100)
      const emitted = wrapper.emitted('upload-success')
      expect(emitted).toBeTruthy()
      expect(emitted && emitted[0]).toEqual([mockResponse])
    })

    it('应该正确处理上传失败', async () => {
      const wrapper = mount(ResumeUpload)
      const mockMessage = vi.spyOn(ElMessage, 'error')
      const error = new Error('上传失败')
      
      await wrapper.vm.handleError(error)
      
      expect(wrapper.vm.uploadProgress).toBe(0)
      expect(mockMessage).toHaveBeenCalledWith('上传失败，请重试')
    })
  })

  describe('中文提示信息', () => {
    it('应该显示中文文件类型提示', () => {
      const wrapper = mount(ResumeUpload)
      expect(wrapper.find('.el-upload__tip').text()).toBe('支持PDF、Word、Excel格式，单个文件不超过100MB')
    })

    it('应该显示中文上传按钮文本', () => {
      const wrapper = mount(ResumeUpload)
      expect(wrapper.find('.el-button').text()).toBe('选择简历文件')
    })
  })
})
