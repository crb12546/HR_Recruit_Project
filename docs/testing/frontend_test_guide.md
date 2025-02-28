# 前端测试指南

## 测试环境配置

### 安装依赖
```bash
cd frontend
npm install
```

### 测试工具
前端测试使用以下工具：
- Jest：JavaScript测试框架
- Vue Test Utils：Vue组件测试工具
- @vue/test-utils：Vue组件测试工具的官方库

## 组件测试

### 组件测试目录结构
```
frontend/
  ├── tests/
  │   ├── unit/
  │   │   ├── components/
  │   │   │   ├── resume/
  │   │   │   ├── job/
  │   │   │   ├── interview/
  │   │   │   └── onboarding/
  │   │   └── ...
  │   └── ...
  └── ...
```

### 运行组件测试
```bash
cd frontend
npm run test:unit
```

### 测试单个组件
```bash
cd frontend
npm run test:unit -- -t "组件名称"
```

## 测试示例

### 简历上传组件测试
```javascript
import { shallowMount } from '@vue/test-utils'
import ResumeUpload from '@/components/resume/ResumeUpload.vue'

describe('ResumeUpload.vue', () => {
  it('渲染上传按钮', () => {
    const wrapper = shallowMount(ResumeUpload)
    expect(wrapper.find('button').text()).toMatch('上传简历')
  })

  it('选择文件后触发上传事件', async () => {
    const wrapper = shallowMount(ResumeUpload)
    
    // 模拟文件选择
    const file = new File([''], 'resume.pdf', { type: 'application/pdf' })
    const input = wrapper.find('input[type="file"]')
    
    // 设置文件并触发change事件
    Object.defineProperty(input.element, 'files', {
      value: [file]
    })
    await input.trigger('change')
    
    // 验证上传事件
    expect(wrapper.emitted('upload')).toBeTruthy()
    expect(wrapper.emitted('upload')[0][0]).toEqual(file)
  })
})
```

### 职位列表组件测试
```javascript
import { shallowMount } from '@vue/test-utils'
import JobList from '@/components/job/JobList.vue'

describe('JobList.vue', () => {
  it('渲染职位列表', () => {
    const jobs = [
      { id: 1, position_name: '前端开发工程师', department: '技术部' },
      { id: 2, position_name: '后端开发工程师', department: '技术部' }
    ]
    
    const wrapper = shallowMount(JobList, {
      propsData: { jobs }
    })
    
    // 验证职位列表渲染
    expect(wrapper.findAll('.job-item').length).toBe(2)
    expect(wrapper.find('.job-item:first-child .position').text()).toContain('前端开发工程师')
  })
})
```

## 模拟API请求

### 使用Jest模拟Axios
```javascript
import axios from 'axios'
import JobList from '@/components/job/JobList.vue'

// 模拟axios
jest.mock('axios')

describe('JobList.vue with API', () => {
  it('加载职位数据', async () => {
    // 模拟API响应
    const mockJobs = [
      { id: 1, position_name: '前端开发工程师', department: '技术部' }
    ]
    
    axios.get.mockResolvedValue({ data: mockJobs })
    
    const wrapper = shallowMount(JobList)
    
    // 等待异步操作完成
    await wrapper.vm.$nextTick()
    
    // 验证数据加载
    expect(wrapper.vm.jobs).toEqual(mockJobs)
  })
})
```

## 测试覆盖率

### 生成测试覆盖率报告
```bash
cd frontend
npm run test:unit -- --coverage
```

### 覆盖率目标
- 组件测试覆盖率目标：80%
- 关键业务组件覆盖率目标：90%

## 常见问题

### 组件渲染问题
如果组件无法正确渲染，请检查：
1. 组件依赖是否正确导入
2. 组件props是否正确传递
3. 组件内部状态是否正确初始化

### 事件触发问题
如果组件事件无法正确触发，请检查：
1. 事件名称是否正确
2. 事件处理函数是否正确绑定
3. 事件参数是否正确传递

### 异步测试问题
如果异步测试失败，请检查：
1. 是否使用了`async/await`或`done`回调
2. 是否等待了组件更新（使用`$nextTick`或`flush-promises`）
3. 是否正确模拟了API响应

## 最佳实践

1. 每个组件都应该有对应的测试文件
2. 测试应该覆盖组件的所有主要功能
3. 使用模拟数据进行测试，避免依赖外部API
4. 测试应该独立且可重复执行
5. 定期运行测试并检查覆盖率报告
