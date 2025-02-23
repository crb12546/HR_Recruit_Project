import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { ElMessage } from 'element-plus'
import JobRequirementForm from '@/components/job/JobRequirementForm.vue'
import ResumeUpload from '@/components/resume/ResumeUpload.vue'
import ResumeList from '@/components/resume/ResumeList.vue'
import InterviewSchedule from '@/components/interview/InterviewSchedule.vue'
import { useJobStore } from '@/store/job'
import { useResumeStore } from '@/store/resume'

describe('完整招聘流程测试', () => {
    beforeEach(() => {
        setActivePinia(createPinia())
    })

    it('应该完成完整的招聘流程', async () => {
        // 1. 创建招聘需求
        const jobForm = mount(JobRequirementForm)
        const jobData = {
            position_name: 'Python高级工程师',
            department: '技术部',
            responsibilities: '负责后端微服务架构设计和开发',
            requirements: '1. 精通Python开发，5年以上经验\n2. 熟悉微服务架构\n3. 具有大型项目经验',
            salary_range: '35k-50k',
            location: '上海'
        }
        
        await jobForm.setData({ form: jobData })
        const jobStore = useJobStore()
        const mockCreateJob = vi.spyOn(jobStore, 'createJob')
        mockCreateJob.mockResolvedValue({ id: 1, ...jobData })
        
        await jobForm.find('button[type="submit"]').trigger('click')
        expect(mockCreateJob).toHaveBeenCalledWith(jobData)
        
        // 2. 上传简历
        const resumeUpload = mount(ResumeUpload)
        const testFile = new File(['test content'], 'senior_dev.pdf', { type: 'application/pdf' })
        const resumeStore = useResumeStore()
        const mockUploadResume = vi.spyOn(resumeStore, 'uploadResume')
        mockUploadResume.mockResolvedValue({
            id: 1,
            talent_portrait: '具有8年Python开发经验的高级工程师'
        })
        
        await resumeUpload.findComponent({ name: 'ElUpload' }).vm.$emit('change', { raw: testFile })
        expect(mockUploadResume).toHaveBeenCalled()
        
        // 3. 查看匹配结果
        const resumeList = mount(ResumeList, {
            props: {
                jobId: 1
            }
        })
        const mockGetMatches = vi.spyOn(jobStore, 'getMatches')
        mockGetMatches.mockResolvedValue([
            {
                resume_id: 1,
                match_score: 0.95,
                match_explanation: '技能和经验完全匹配职位要求'
            }
        ])
        
        await resumeList.vm.$nextTick()
        const matchItems = resumeList.findAll('.match-item')
        expect(matchItems.length).toBeGreaterThan(0)
        
        // 4. 安排面试
        const interviewSchedule = mount(InterviewSchedule)
        const scheduleData = {
            resume_id: 1,
            job_id: 1,
            interviewer_id: 1,
            interview_time: '2025-03-01T14:00:00'
        }
        
        await interviewSchedule.setData({ form: scheduleData })
        const mockScheduleInterview = vi.fn().mockResolvedValue({ id: 1, status: 'scheduled' })
        interviewSchedule.vm.scheduleInterview = mockScheduleInterview
        
        await interviewSchedule.find('button.schedule-btn').trigger('click')
        expect(mockScheduleInterview).toHaveBeenCalledWith(scheduleData)
        
        // 验证整个流程的状态
        expect(ElMessage.success).toHaveBeenCalledWith('面试已成功安排')
    })
})
