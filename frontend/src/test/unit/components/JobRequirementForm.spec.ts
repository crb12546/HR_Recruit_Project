import { describe, it, expect } from 'vitest'
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
    const positionInput = wrapper.find('input[id="position_name"]')
    const departmentInput = wrapper.find('input[id="department"]')
    const responsibilitiesInput = wrapper.find('textarea[id="responsibilities"]')
    const requirementsInput = wrapper.find('textarea[id="requirements"]')
    const salaryInput = wrapper.find('input[id="salary_range"]')
    const locationInput = wrapper.find('input[id="location"]')

    await positionInput.setValue('Python后端工程师')
    await departmentInput.setValue('技术部')
    await responsibilitiesInput.setValue('负责后端API开发和维护')
    await requirementsInput.setValue('熟悉Python, FastAPI框架\n3年以上相关开发经验')
    await salaryInput.setValue('25k-35k')
    await locationInput.setValue('上海')
    
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
    const labels = wrapper.findAll('label')
    const labelTexts = {
      'position_name': '职位名称',
      'department': '部门',
      'responsibilities': '岗位职责',
      'requirements': '任职要求',
      'salary_range': '薪资范围',
      'location': '工作地点'
    }

    for (const [id, text] of Object.entries(labelTexts)) {
      const label = labels.find(l => l.attributes('for') === id)
      expect(label?.text()).toBe(text)
    }
    
    // 验证提交按钮存在
    expect(wrapper.find('button[type="primary"]').text()).toBe('提交')
  })
})
