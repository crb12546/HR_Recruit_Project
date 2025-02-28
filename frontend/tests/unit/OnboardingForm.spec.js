import { shallowMount } from '@vue/test-utils'
import { nextTick } from 'vue'
import OnboardingForm from '@/components/onboarding/OnboardingForm.vue'
import { ElMessage } from 'element-plus'

// 模拟Element Plus组件
jest.mock('element-plus', () => ({
  ElMessage: {
    success: jest.fn(),
    error: jest.fn()
  }
}))

// 模拟vue-router
const mockRoute = {
  params: {}
}

const mockRouter = {
  push: jest.fn()
}

// 模拟fetch API
global.fetch = jest.fn()

describe('OnboardingForm.vue', () => {
  let wrapper
  
  beforeEach(() => {
    // 重置所有模拟
    jest.clearAllMocks()
    
    // 重置路由参数
    mockRoute.params = {}
    
    // 模拟成功的API响应
    global.fetch.mockImplementation((url) => {
      if (url.includes('/resumes')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({
            resumes: [
              { id: 1, candidate_name: '张三' },
              { id: 2, candidate_name: '李四' }
            ]
          })
        })
      } else if (url.includes('/jobs')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({
            jobs: [
              { id: 1, position_name: 'Python工程师' },
              { id: 2, position_name: '前端工程师' }
            ]
          })
        })
      } else if (url.includes('/onboardings') && !url.includes('/onboardings/')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({
            id: 1,
            resume_id: 1,
            job_requirement_id: 1,
            department: '技术部',
            position: 'Python工程师',
            status: 'pending'
          })
        })
      }
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({})
      })
    })
    
    // 挂载组件
    wrapper = shallowMount(OnboardingForm, {
      global: {
        mocks: {
          $route: mockRoute,
          $router: mockRouter
        }
      }
    })
  })
  
  it('初始化时应该加载候选人和职位列表', async () => {
    // 等待异步操作完成
    await nextTick()
    
    // 验证fetch被调用
    expect(global.fetch).toHaveBeenCalledWith('/api/v1/resumes')
    expect(global.fetch).toHaveBeenCalledWith('/api/v1/jobs')
    
    // 验证数据加载
    expect(wrapper.vm.resumes.length).toBe(2)
    expect(wrapper.vm.jobs.length).toBe(2)
  })
  
  it('编辑模式下应该加载入职记录详情', async () => {
    // 模拟编辑模式
    mockRoute.params = { id: '1' }
    
    // 模拟入职记录详情响应
    global.fetch.mockImplementation((url) => {
      if (url === '/api/v1/onboardings/1') {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({
            id: 1,
            resume_id: 1,
            job_requirement_id: 1,
            department: '技术部',
            position: 'Python工程师',
            salary: '30k',
            offer_date: '2025-03-01T00:00:00',
            start_date: '2025-04-01T00:00:00',
            probation_end_date: '2025-07-01T00:00:00',
            status: 'pending',
            notes: '测试备注'
          })
        })
      }
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({})
      })
    })
    
    // 重新挂载组件
    wrapper = shallowMount(OnboardingForm, {
      global: {
        mocks: {
          $route: mockRoute,
          $router: mockRouter
        }
      }
    })
    
    // 等待异步操作完成
    await nextTick()
    
    // 验证fetch被调用
    expect(global.fetch).toHaveBeenCalledWith('/api/v1/onboardings/1')
    
    // 验证表单数据
    expect(wrapper.vm.form.resume_id).toBe(1)
    expect(wrapper.vm.form.job_requirement_id).toBe(1)
    expect(wrapper.vm.form.department).toBe('技术部')
    expect(wrapper.vm.form.position).toBe('Python工程师')
    expect(wrapper.vm.form.status).toBe('pending')
  })
  
  it('表单验证应该正确工作', async () => {
    // 设置表单引用
    wrapper.vm.formRef = {
      validate: jest.fn((callback) => {
        callback(false) // 模拟验证失败
      })
    }
    
    // 调用提交方法
    await wrapper.vm.submitForm()
    
    // 验证表单验证被调用
    expect(wrapper.vm.formRef.validate).toHaveBeenCalled()
    
    // 验证fetch没有被调用（因为验证失败）
    expect(global.fetch).not.toHaveBeenCalledWith('/api/v1/onboardings', expect.objectContaining({
      method: 'POST'
    }))
  })
  
  it('创建模式下应该成功提交入职记录', async () => {
    // 设置表单数据
    await wrapper.setData({
      form: {
        resume_id: 1,
        job_requirement_id: 1,
        department: '技术部',
        position: 'Python工程师',
        salary: '30k',
        offer_date: '2025-03-01T00:00:00',
        start_date: '2025-04-01T00:00:00',
        probation_end_date: '2025-07-01T00:00:00',
        status: 'pending',
        notes: '测试备注',
        generate_tasks: true
      }
    })
    
    // 设置表单引用
    wrapper.vm.formRef = {
      validate: jest.fn((callback) => {
        callback(true) // 模拟验证成功
      })
    }
    
    // 调用提交方法
    await wrapper.vm.submitForm()
    
    // 验证fetch被调用
    expect(global.fetch).toHaveBeenCalledWith('/api/v1/onboardings', expect.objectContaining({
      method: 'POST',
      headers: expect.objectContaining({
        'Content-Type': 'application/json'
      }),
      body: expect.any(String)
    }))
    
    // 验证成功消息
    expect(ElMessage.success).toHaveBeenCalledWith('创建入职记录成功')
    
    // 验证路由导航
    expect(mockRouter.push).toHaveBeenCalledWith('/onboardings')
  })
  
  it('编辑模式下应该成功更新入职记录', async () => {
    // 模拟编辑模式
    mockRoute.params = { id: '1' }
    
    // 重新挂载组件
    wrapper = shallowMount(OnboardingForm, {
      global: {
        mocks: {
          $route: mockRoute,
          $router: mockRouter
        }
      }
    })
    
    // 设置表单数据
    await wrapper.setData({
      form: {
        resume_id: 1,
        job_requirement_id: 1,
        department: '技术部',
        position: 'Python工程师',
        salary: '32k', // 更新薪资
        status: 'in_progress', // 更新状态
        notes: '更新备注'
      }
    })
    
    // 设置表单引用
    wrapper.vm.formRef = {
      validate: jest.fn((callback) => {
        callback(true) // 模拟验证成功
      })
    }
    
    // 调用提交方法
    await wrapper.vm.submitForm()
    
    // 验证fetch被调用
    expect(global.fetch).toHaveBeenCalledWith('/api/v1/onboardings/1', expect.objectContaining({
      method: 'PUT',
      headers: expect.objectContaining({
        'Content-Type': 'application/json'
      }),
      body: expect.any(String)
    }))
    
    // 验证成功消息
    expect(ElMessage.success).toHaveBeenCalledWith('更新入职记录成功')
    
    // 验证路由导航
    expect(mockRouter.push).toHaveBeenCalledWith('/onboardings')
  })
  
  it('提交失败时应该显示错误消息', async () => {
    // 模拟提交失败
    global.fetch.mockImplementation((url) => {
      if (url === '/api/v1/onboardings') {
        return Promise.resolve({
          ok: false,
          json: () => Promise.resolve({ detail: '创建失败' })
        })
      }
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({})
      })
    })
    
    // 设置表单数据
    await wrapper.setData({
      form: {
        resume_id: 1,
        job_requirement_id: 1,
        department: '技术部',
        position: 'Python工程师',
        status: 'pending'
      }
    })
    
    // 设置表单引用
    wrapper.vm.formRef = {
      validate: jest.fn((callback) => {
        callback(true) // 模拟验证成功
      })
    }
    
    // 调用提交方法
    await wrapper.vm.submitForm()
    
    // 验证错误消息
    expect(ElMessage.error).toHaveBeenCalledWith('创建入职记录失败: 创建失败')
  })
  
  it('点击取消按钮应该返回列表页面', async () => {
    // 找到取消按钮并点击
    const cancelButton = wrapper.find('button:last-child')
    await cancelButton.trigger('click')
    
    // 验证路由导航
    expect(mockRouter.push).toHaveBeenCalledWith('/onboardings')
  })
})
