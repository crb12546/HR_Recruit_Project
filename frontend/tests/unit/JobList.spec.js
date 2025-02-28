import { shallowMount } from '@vue/test-utils'
import { nextTick } from 'vue'
import JobList from '@/components/job/JobList.vue'
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

describe('JobList.vue', () => {
  let wrapper
  
  beforeEach(() => {
    // 重置所有模拟
    jest.clearAllMocks()
    
    // 模拟成功的职位列表响应
    global.fetch.mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({
        jobs: [
          {
            id: 1,
            position_name: 'Python高级工程师',
            department: '技术部',
            salary_range: '25k-35k',
            status: 'open',
            created_at: '2025-02-01T00:00:00'
          },
          {
            id: 2,
            position_name: '前端开发工程师',
            department: '技术部',
            salary_range: '20k-30k',
            status: 'open',
            created_at: '2025-02-05T00:00:00'
          }
        ]
      })
    })
    
    // 挂载组件
    wrapper = shallowMount(JobList, {
      global: {
        mocks: {
          $router: mockRouter
        }
      }
    })
  })
  
  it('初始化时应该加载职位列表', async () => {
    // 等待异步操作完成
    await nextTick()
    
    // 验证fetch被调用
    expect(global.fetch).toHaveBeenCalledWith('/api/v1/jobs')
    
    // 验证职位列表数据
    expect(wrapper.vm.jobs.length).toBe(2)
    expect(wrapper.vm.jobs[0].position_name).toBe('Python高级工程师')
  })
  
  it('点击创建按钮应该导航到创建页面', async () => {
    // 找到创建按钮并点击
    const createButton = wrapper.find('.job-list-header button')
    await createButton.trigger('click')
    
    // 验证路由导航
    expect(mockRouter.push).toHaveBeenCalledWith('/jobs/new')
  })
  
  it('点击查看详情应该导航到详情页面', async () => {
    // 设置职位数据
    await wrapper.setData({
      jobs: [
        {
          id: 1,
          position_name: 'Python高级工程师',
          department: '技术部',
          status: 'open'
        }
      ]
    })
    
    // 找到详情按钮并点击
    const detailButton = wrapper.find('.view-job-btn')
    await detailButton.trigger('click')
    
    // 验证路由导航
    expect(mockRouter.push).toHaveBeenCalledWith('/jobs/1')
  })
  
  it('获取职位列表失败时应该显示错误消息', async () => {
    // 模拟获取失败
    global.fetch.mockResolvedValue({
      ok: false,
      json: () => Promise.resolve({ detail: '获取失败' })
    })
    
    // 重新挂载组件
    wrapper = shallowMount(JobList, {
      global: {
        mocks: {
          $router: mockRouter
        }
      }
    })
    
    // 等待异步操作完成
    await nextTick()
    
    // 验证错误消息
    expect(ElMessage.error).toHaveBeenCalledWith('获取职位列表失败')
    
    // 验证加载状态
    expect(wrapper.vm.loading).toBe(false)
  })
  
  it('网络错误时应该显示错误消息并使用模拟数据', async () => {
    // 模拟网络错误
    global.fetch.mockRejectedValue(new Error('网络错误'))
    
    // 重新挂载组件
    wrapper = shallowMount(JobList, {
      global: {
        mocks: {
          $router: mockRouter
        }
      }
    })
    
    // 等待异步操作完成
    await nextTick()
    
    // 验证错误消息
    expect(ElMessage.error).toHaveBeenCalledWith('获取职位列表失败')
    
    // 验证使用了模拟数据
    expect(wrapper.vm.jobs.length).toBeGreaterThan(0)
    
    // 验证加载状态
    expect(wrapper.vm.loading).toBe(false)
  })
})
