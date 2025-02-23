import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { ElForm, ElMessage } from 'element-plus'
import JobRequirementForm from '@/components/job/JobRequirementForm.vue'

describe('JobRequirementForm Component', () => {
  it('should validate required fields', async () => {
    const wrapper = mount(JobRequirementForm)
    const form = wrapper.findComponent(ElForm)
    
    // Submit empty form
    await wrapper.find('button[type="submit"]').trigger('click')
    
    // Check validation messages
    const errorMessages = wrapper.findAll('.el-form-item__error')
    expect(errorMessages.length).toBeGreaterThan(0)
    expect(errorMessages.some(msg => msg.text().includes('职位名称不能为空'))).toBe(true)
  })

  it('should submit form successfully', async () => {
    const wrapper = mount(JobRequirementForm)
    
    // Fill form data
    await wrapper.setData({
      form: {
        position_name: 'Python后端工程师',
        department: '技术部',
        responsibilities: '负责后端API开发和维护',
        requirements: '熟悉Python, FastAPI框架\n3年以上相关开发经验',
        salary_range: '25k-35k',
        location: '上海'
      }
    })
    
    const mockSubmit = vi.fn().mockResolvedValue({ id: 1 })
    wrapper.vm.submitForm = mockSubmit
    
    // Submit form
    await wrapper.find('button[type="submit"]').trigger('click')
    
    expect(mockSubmit).toHaveBeenCalled()
    expect(wrapper.emitted('submit-success')).toBeTruthy()
  })
})
