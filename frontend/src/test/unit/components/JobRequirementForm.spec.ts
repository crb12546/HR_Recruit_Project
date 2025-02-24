import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { ElMessage } from 'element-plus'
import JobRequirementForm from '@/components/job/JobRequirementForm.vue'

interface JobFormData {
  position_name: string;
  department: string;
  responsibilities: string;
  requirements: string;
  salary_range: string;
  location: string;
}

type JobFormKey = keyof JobFormData;

describe('职位需求表单组件', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  const mountForm = () => {
    return mount(JobRequirementForm, {
      props: {
        form: {
          position_name: '',
          department: '',
          responsibilities: '',
          requirements: '',
          salary_range: '',
          location: ''
        }
      }
    })
  }

  it('应该验证必填字段', async () => {
    const wrapper = mountForm()
    
    // 尝试提交空表单
    await wrapper.find('.submit-button').trigger('click')
    await wrapper.vm.$nextTick()
    
    // 验证错误消息被显示
    expect(ElMessage.error).toHaveBeenCalledWith('表单验证失败，请检查必填项')
    expect(wrapper.emitted()).not.toHaveProperty('submit-success')
  })

  it('应该成功提交表单', async () => {
    const testData = {
      position_name: 'Python后端工程师',
      department: '技术部',
      responsibilities: '负责后端API开发和维护',
      requirements: '熟悉Python, FastAPI框架\n3年以上相关开发经验',
      salary_range: '25k-35k',
      location: '上海'
    }
    
    const wrapper = mount(JobRequirementForm)
    const vm = wrapper.vm as any
    
    // 设置表单数据
    const formData = testData as JobFormData
    (Object.keys(formData) as JobFormKey[]).forEach((key) => {
      vm.form[key] = formData[key]
    })
    await wrapper.vm.$nextTick()
    
    // 提交表单
    await wrapper.find('.submit-button').trigger('click')
    await wrapper.vm.$nextTick()
    
    // 验证提交事件
    const emitted = wrapper.emitted()
    expect(emitted).toHaveProperty('submit-success')
    const submitEvent = emitted['submit-success'] as any[][]
    expect(submitEvent[0][0]).toEqual(testData)
  })

  it('应该正确显示所有表单字段', () => {
    const wrapper = mountForm()
    const expectedLabels = [
      '职位名称',
      '部门',
      '岗位职责',
      '任职要求',
      '薪资范围',
      '工作地点'
    ]

    const labels = wrapper.findAll('.el-form-item__label')
    expect(labels).toHaveLength(expectedLabels.length)
    labels.forEach((label, index) => {
      expect(label.text()).toBe(expectedLabels[index])
    })
    
    // 验证提交按钮存在
    expect(wrapper.find('button.submit-button').exists()).toBe(true)
    expect(wrapper.find('button.submit-button').text()).toBe('提交')
  })
})
