import { describe, it, expect, vi, beforeEach } from 'vitest'
import { nextTick } from 'vue'
import { mount } from '@vue/test-utils'
import { ElMessage } from 'element-plus'
import JobRequirementForm from '@/components/job/JobRequirementForm.vue'

// 模拟Element Plus组件
vi.mock('element-plus', () => ({
  ElMessage: {
    error: vi.fn(),
    success: vi.fn()
  }
}))

describe('职位需求表单组件', () => {
  const mockValidate = vi.fn()
  
  const mockComponents = {
    'el-form': {
      template: '<form><slot></slot></form>',
      methods: {
        validate: mockValidate
      }
    },
    'el-form-item': {
      template: '<div class="el-form-item"><label v-if="$attrs.label">{{ $attrs.label }}</label><slot></slot></div>',
      inheritAttrs: true
    },
    'el-input': {
      template: '<input :value="modelValue" @input="$emit(\'update:modelValue\', $event.target.value)" />',
      props: ['modelValue'],
      emits: ['update:modelValue']
    },
    'el-button': {
      template: '<button type="button" class="el-button" @click="$emit(\'click\')"><slot></slot></button>',
      emits: ['click']
    }
  }

  beforeEach(() => {
    vi.clearAllMocks()
    mockValidate.mockReset()
  })

  it('应该验证必填字段', async () => {
    mockValidate.mockRejectedValue(new Error('验证失败'))
    
    const wrapper = mount(JobRequirementForm, {
      global: {
        stubs: mockComponents
      }
    })
    
    // 尝试提交空表单
    await wrapper.find('.el-button').trigger('click')
    
    // 验证错误消息
    expect(ElMessage.error).toHaveBeenCalledWith('表单验证失败，请检查必填项')
  })

  it('应该成功提交表单', async () => {
    mockValidate.mockResolvedValue(true)
    
    const wrapper = mount(JobRequirementForm, {
      global: {
        stubs: mockComponents
      }
    })
    
    const formData = {
      position_name: 'Python后端工程师',
      department: '技术部',
      responsibilities: '负责后端API开发和维护',
      requirements: '熟悉Python, FastAPI框架3年以上相关开发经验',
      salary_range: '25k-35k',
      location: '上海'
    }

    // 更新表单数据
    const inputs = wrapper.findAll('input')
    for (let i = 0; i < inputs.length; i++) {
      await inputs[i].setValue(Object.values(formData)[i])
    }
    await nextTick()

    // 提交表单
    await wrapper.find('.el-button').trigger('click')
    
    // 验证提交事件
    const emitted = wrapper.emitted('submit-success')
    expect(emitted).toBeTruthy()
    expect(emitted && emitted[0][0]).toEqual(formData)
  })

  it('应该正确显示所有表单字段', () => {
    const wrapper = mount(JobRequirementForm, {
      global: {
        stubs: mockComponents
      }
    })
    
    // 验证所有必要的表单项都存在
    const formItems = wrapper.findAll('.el-form-item')
    const labels = formItems
      .map(item => item.attributes('label'))
      .filter(Boolean)
    
    expect(labels).toEqual(['职位名称', '部门', '岗位职责', '任职要求', '薪资范围', '工作地点'])
    
    // 验证提交按钮存在
    expect(wrapper.find('.el-button').exists()).toBe(true)
  })
})
