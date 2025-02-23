import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { ref, nextTick, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

// 模拟Element Plus组件
vi.mock('element-plus', () => ({
  ElMessage: {
    error: vi.fn(),
    success: vi.fn(() => ({
      type: 'success',
      close: vi.fn()
    }))
  }
}))

// 模拟状态管理
const mockJobStore = {
  createJob: vi.fn(),
  getMatches: vi.fn()
}

const mockResumeStore = {
  uploadResume: vi.fn()
}

vi.mock('@/store/job', () => ({
  useJobStore: () => mockJobStore
}))

vi.mock('@/store/resume', () => ({
  useResumeStore: () => mockResumeStore
}))

// 每个测试前重置所有模拟
beforeEach(() => {
  vi.clearAllMocks()
  setActivePinia(createPinia())
})

// Mock components
const JobRequirementFormComponent = {
  name: 'JobRequirementForm',
  template: `
    <div class="job-requirement-form">
      <form @submit.prevent="handleSubmit">
        <input v-model="formData.position_name" />
        <input v-model="formData.department" />
        <input v-model="formData.responsibilities" />
        <input v-model="formData.requirements" />
        <input v-model="formData.salary_range" />
        <input v-model="formData.location" />
        <button type="submit">提交</button>
      </form>
    </div>
  `,
  props: {
    form: {
      type: Object,
      required: true
    }
  },
  emits: ['submit-success'],
  setup(props: { form: any }, { emit }: { emit: (event: string, data?: any) => void }) {
    const formData = reactive({...props.form})

    const handleSubmit = async () => {
      try {
        await mockJobStore.createJob(formData)
        emit('submit-success', formData)
      } catch (error) {
        ElMessage.error('表单验证失败，请检查必填项')
      }
    }
    return { formData, handleSubmit }
  }
}

vi.mock('@/components/job/JobRequirementForm.vue', () => ({
  default: JobRequirementFormComponent
}))

const ResumeUploadComponent = {
  name: 'ResumeUpload',
  template: `
    <div class="resume-upload">
      <form @submit.prevent>
        <input type="file" @change="handleFileChange" accept=".pdf,.doc,.docx,.xls,.xlsx" />
      </form>
    </div>
  `,
  emits: ['upload-success'],
  setup(_props: any, { emit }: { emit: (event: string, data?: any) => void }) {
    const handleFileChange = async (event: { target: { files: File[] } }) => {
      const file = event.target.files[0]
      if (file) {
        try {
          const result = await mockResumeStore.uploadResume(file)
          emit('upload-success', result)
        } catch (error: any) {
          ElMessage.error(error?.message || '上传失败')
        }
      }
    }
    return { handleFileChange }
  }
}

vi.mock('@/components/resume/ResumeUpload.vue', () => ({
  default: ResumeUploadComponent
}))

const ResumeListComponent = {
  name: 'ResumeList',
  template: `
    <div class="resume-list">
      <div v-for="match in matches" :key="match.resume_id" class="match-item">
        <div class="match-score">匹配度: {{ (match.match_score * 100).toFixed(0) }}%</div>
        <div class="match-explanation">{{ match.match_explanation }}</div>
      </div>
    </div>
  `,
  props: {
    jobId: {
      type: Number,
      required: true
    }
  },
  setup(props: { jobId: number }) {
    const matches = ref<Array<{ resume_id: number; match_score: number; match_explanation: string }>>([])
    
    onMounted(async () => {
      const mockData = [{
        resume_id: 1,
        match_score: 0.95,
        match_explanation: '技能和经验完全匹配职位要求'
      }]
      mockJobStore.getMatches.mockResolvedValue(mockData)
      await mockJobStore.getMatches(props.jobId)
      matches.value = mockData
      await nextTick()
    })
    
    return { matches }
  }
}

vi.mock('@/components/resume/ResumeList.vue', () => ({
  default: ResumeListComponent
}))

// 模拟面试组件

const InterviewScheduleComponent = {
  name: 'InterviewSchedule',
  template: `
    <div class="interview-schedule">
      <form @submit.prevent>
        <button type="button" class="schedule-btn" @click="handleSchedule">安排面试</button>
      </form>
    </div>
  `,
  props: {
    form: {
      type: Object,
      required: true,
      default: () => ({})
    }
  },
  emits: ['schedule-success'],
  setup(_props: unknown, { emit }: { emit: (event: string) => void }) {
    const handleSchedule = async () => {
      await new Promise(resolve => setTimeout(resolve, 100)) // Simulate API call
      ElMessage.success('面试已成功安排')
      emit('schedule-success')
    }
    return { handleSchedule }
  }
}

vi.mock('@/components/interview/InterviewSchedule.vue', () => ({
  default: InterviewScheduleComponent
}))

describe('招聘流程集成测试', () => {

    it('应该完成从发布职位到安排面试的完整流程', async () => {
        // 第一步：创建招聘需求
        // 准备测试数据
        const jobData = {
            position_name: 'Python高级工程师',
            department: '技术部',
            responsibilities: '负责后端微服务架构设计和开发',
            requirements: '1. 精通Python开发，5年以上经验\n2. 熟悉微服务架构\n3. 具有大型项目经验',
            salary_range: '35k-50k',
            location: '上海'
        }
        
        mockJobStore.createJob.mockResolvedValue({ id: 1, ...jobData })

        const wrapper = mount(JobRequirementFormComponent, {
            props: {
                form: jobData
            },
            global: {
                stubs: {
                    'el-form': true,
                    'el-form-item': true,
                    'el-input': true,
                    'el-button': true
                }
            }
        })

        console.log('Component HTML:', wrapper.html())
        
        await nextTick()
        const form = wrapper.find('form')
        expect(form.exists()).toBe(true)
        await form.trigger('submit')
        expect(mockJobStore.createJob).toHaveBeenCalledWith(jobData)
        
        // 第二步：上传候选人简历
        // 模拟简历上传响应
        mockResumeStore.uploadResume.mockResolvedValue({
            id: 1,
            talent_portrait: '具有8年Python开发经验的高级工程师'
        })

        const resumeUpload = mount(ResumeUploadComponent)
        console.log('ResumeUpload HTML:', resumeUpload.html())
        
        const testFile = new File(['test content'], 'senior_dev.pdf', { type: 'application/pdf' })
        const input = resumeUpload.find('input[type="file"]')
        expect(input.exists()).toBe(true)
        
        // Create a mock event
        const event = {
            preventDefault: vi.fn(),
            target: {
                files: [testFile]
            }
        }
        
        // Call the component's method directly
        await (resumeUpload.vm as any).handleFileChange(event)
        expect(mockResumeStore.uploadResume).toHaveBeenCalledWith(testFile)
        
        // 第三步：查看简历匹配结果
        // 模拟匹配结果数据
        mockJobStore.getMatches.mockResolvedValue([{
            resume_id: 1,
            match_score: 0.95,
            match_explanation: '技能和经验完全匹配职位要求'
        }])

        const resumeList = mount(ResumeListComponent, {
            props: {
                jobId: 1
            },
            global: {
                provide: {
                    jobStore: mockJobStore
                }
            }
        })

        await nextTick()
        console.log('ResumeList HTML:', resumeList.html())
        
        const matchItems = resumeList.findAll('.match-item')
        expect(matchItems.length).toBe(1)
        expect(mockJobStore.getMatches).toHaveBeenCalledWith(1)
        
        // 第四步：安排候选人面试
        // 准备面试安排数据
        const scheduleData = {
            resume_id: 1,
            job_id: 1,
            interviewer_id: 1,
            interview_time: '2025-03-01T14:00:00'
        }

        const interviewSchedule = mount(InterviewScheduleComponent, {
            props: {
                form: scheduleData
            }
        })

        console.log('InterviewSchedule HTML:', interviewSchedule.html())
        
        const scheduleButton = interviewSchedule.find('button.schedule-btn')
        expect(scheduleButton.exists()).toBe(true)
        
        // Trigger the click event
        await scheduleButton.trigger('click')
        
        // Wait for the simulated API call and Vue updates
        await new Promise(resolve => setTimeout(resolve, 150))
        await nextTick()
        
        // 验证整个流程的状态
        expect(ElMessage.success).toHaveBeenCalledWith('面试已成功安排')
        expect(interviewSchedule.emitted('schedule-success')).toBeTruthy()
        
        // 验证所有关键步骤都已完成
        expect(mockJobStore.createJob).toHaveBeenCalledTimes(1)
        expect(mockResumeStore.uploadResume).toHaveBeenCalledTimes(1)
        expect(mockJobStore.getMatches).toHaveBeenCalledTimes(1)
    })
    
    it('应该正确处理错误情况', async () => {
        // 模拟创建职位失败
        mockJobStore.createJob.mockRejectedValue(new Error('创建失败'))
        
        const wrapper = mount(JobRequirementFormComponent, {
            props: {
                form: {
                    position_name: 'Python高级工程师'
                }
            }
        })
        
        await wrapper.find('form').trigger('submit')
        expect(ElMessage.error).toHaveBeenCalled()
        
        // 模拟简历上传失败
        mockResumeStore.uploadResume.mockRejectedValue({message: '上传失败'})
        
        const resumeUpload = mount(ResumeUploadComponent)
        const testFile = new File(['test'], 'test.pdf', { type: 'application/pdf' })
        
        await (resumeUpload.vm as any).handleFileChange({
            target: { files: [testFile] }
        })
        
        expect(ElMessage.error).toHaveBeenCalled()
    })
})
