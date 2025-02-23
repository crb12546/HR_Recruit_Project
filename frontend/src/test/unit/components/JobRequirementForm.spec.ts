import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import JobRequirementForm from '@/components/job/JobRequirementForm.vue'

describe('职位需求表单组件', () => {
  it('应该验证必填字段', async () => {
    const wrapper = mount(JobRequirementForm)
    
    // 尝试提交空表单
    await wrapper.find('button[type="primary"]').trigger('click')
    
    // 验证错误信息
    const errorMessages = wrapper.findAll('.el-form-item__error')
    expect(errorMessages.length).toBe(3) // 职位名称、岗位职责、任职要求都是必填
    expect(errorMessages[0].text()).toBe('职位名称不能为空')
    expect(errorMessages[1].text()).toBe('岗位职责不能为空')
    expect(errorMessages[2].text()).toBe('任职要求不能为空')
  })

  it('应该成功提交表单', async () => {
    const wrapper = mount(JobRequirementForm)
    
    // 填写表单数据
    await wrapper.find('input[id="position_name"]').setValue('Python后端工程师')
    await wrapper.find('input[id="department"]').setValue('技术部')
    await wrapper.find('textarea[id="responsibilities"]').setValue('负责后端API开发和维护')
    await wrapper.find('textarea[id="requirements"]').setValue('熟悉Python, FastAPI框架\n3年以上相关开发经验')
    await wrapper.find('input[id="salary_range"]').setValue('25k-35k')
    await wrapper.find('input[id="location"]').setValue('上海')
    
    // 提交表单
    await wrapper.find('button[type="primary"]').trigger('click')
    
    // 验证提交事件
    const emitted = wrapper.emitted('submit-success')
    expect(emitted).toBeTruthy()
    expect(emitted && emitted[0][0]).toEqual({
      position_name: 'Python后端工程师',
      department: '技术部',
      responsibilities: '负责后端API开发和维护',
      requirements: '熟悉Python, FastAPI框架\n3年以上相关开发经验',
      salary_range: '25k-35k',
      location: '上海'
    })
  })

  it('应该正确显示所有表单字段', () => {
    const wrapper = mount(JobRequirementForm)
    
    // 验证所有必要的表单项都存在
    expect(wrapper.find('label[for="position_name"]').text()).toBe('职位名称')
    expect(wrapper.find('label[for="department"]').text()).toBe('部门')
    expect(wrapper.find('label[for="responsibilities"]').text()).toBe('岗位职责')
    expect(wrapper.find('label[for="requirements"]').text()).toBe('任职要求')
    expect(wrapper.find('label[for="salary_range"]').text()).toBe('薪资范围')
    expect(wrapper.find('label[for="location"]').text()).toBe('工作地点')
    
    // 验证提交按钮存在
    expect(wrapper.find('button[type="primary"]').text()).toBe('提交')
  })
})
