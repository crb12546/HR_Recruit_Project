import { shallowMount } from '@vue/test-utils'
import { nextTick } from 'vue'
import InterviewSchedule from '@/components/interview/InterviewSchedule.vue'
import { ElMessage } from 'element-plus'

// 模拟Element Plus组件
jest.mock('element-plus', () => ({
  ElMessage: {
    success: jest.fn(),
    error: jest.fn()
  }
}))

// 模拟vue-router
const mockRouter = {
  push: jest.fn()
}

// 模拟fetch API
global.fetch = jest.fn()

describe('InterviewSchedule.vue', () => {
  let wrapper
  
  beforeEach(() => {
    // 重置所有模拟
    jest.clearAllMocks()
    
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
      } else if (url.includes('/users')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({
            users: [
              { id: 1, username: '面试官1', role: 'interviewer' },
              { id: 2, username: '面试官2', role: 'interviewer' }
            ]
          })
        })
      } else if (url.includes('/interviews')) {
        return Promise.resolve({
          ok: true,
          json: () => Promise.resolve({
            id: 1,
            resume_id: 1,
            job_requirement_id: 1,
            interviewer_id: 1,
            interview_time: '2025-03-15T10:00:00',
            interview_type: '技术面试',
            status: 'scheduled'
          })
        })
      }
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve({})
      })
    })
    
    // 挂载组件
    wrapper = shallowMount(InterviewSchedule, {
      global: {
        mocks: {
          $router: mockRouter
        }
      }
    })
  })
  
  it('初始化时应该加载候选人、职位和面试官列表', async () => {
    // 等待异步操作完成
    await nextTick()
    
    // 验证fetch被调用
    expect(global.fetch).toHaveBeenCalledWith('/api/v1/resumes')
    expect(global.fetch).toHaveBeenCalledWith('/api/v1/jobs')
    expect(global.fetch).toHaveBeenCalledWith('/api/v1/users?role=interviewer')
    
    // 验证数据加载
    expect(wrapper.vm.resumes.length).toBe(2)
    expect(wrapper.vm.jobs.length).toBe(2)
    expect(wrapper.vm.interviewers.length).toBe(2)
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
    expect(global.fetch).not.toHaveBeenCalledWith('/api/v1/interviews')
  })
  
  it('应该成功提交面试安排', async () => {
    // 设置表单数据
    await wrapper.setData({
      form: {
        resume_id: 1,
        job_requirement_id: 1,
        interviewer_id: 1,
        interview_time: '2025-03-15T10:00:00',
        interview_type: '技术面试',
        status: 'scheduled',
        notes: '面试备注'
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
    expect(global.fetch).toHaveBeenCalledWith('/api/v1/interviews', expect.objectContaining({
      method: 'POST',
      headers: expect.objectContaining({
        'Content-Type': 'application/json'
      }),
      body: expect.any(String)
    }))
    
    // 验证成功消息
    expect(ElMessage.success).toHaveBeenCalledWith('面试安排成功')
    
    // 验证路由导航
    expect(mockRouter.push).toHaveBeenCalledWith('/interviews')
  })
  
  it('提交失败时应该显示错误消息', async () => {
    // 模拟提交失败
    global.fetch.mockImplementation((url) => {
      if (url === '/api/v1/interviews') {
        return Promise.resolve({
          ok: false,
          json: () => Promise.resolve({ detail: '安排失败' })
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
        interviewer_id: 1,
        interview_time: '2025-03-15T10:00:00',
        interview_type: '技术面试',
        status: 'scheduled'
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
    expect(ElMessage.error).toHaveBeenCalledWith('安排面试失败: 安排失败')
  })
  
  it('点击取消按钮应该返回列表页面', async () => {
    // 找到取消按钮并点击
    const cancelButton = wrapper.find('.cancel-btn')
    await cancelButton.trigger('click')
    
    // 验证路由导航
    expect(mockRouter.push).toHaveBeenCalledWith('/interviews')
  })
})
