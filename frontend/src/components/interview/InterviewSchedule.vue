<template>
  <div class="interview-schedule">
    <h2>安排面试</h2>
    
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
    >
      <el-form-item label="候选人" prop="resume_id">
        <el-select
          v-model="form.resume_id"
          placeholder="请选择候选人"
          class="resume-select"
          filterable
        >
          <el-option
            v-for="resume in resumes"
            :key="resume.id"
            :label="resume.candidate_name || resume.name"
            :value="resume.id"
          />
        </el-select>
      </el-form-item>
      
      <el-form-item label="职位" prop="job_requirement_id">
        <el-select
          v-model="form.job_requirement_id"
          placeholder="请选择职位"
          class="job-select"
          filterable
        >
          <el-option
            v-for="job in jobs"
            :key="job.id"
            :label="job.position_name || job.title"
            :value="job.id"
          />
        </el-select>
      </el-form-item>
      
      <el-form-item label="面试官" prop="interviewer_id">
        <el-select
          v-model="form.interviewer_id"
          placeholder="请选择面试官"
          class="interviewer-select"
          filterable
        >
          <el-option
            v-for="interviewer in interviewers"
            :key="interviewer.id"
            :label="interviewer.username || interviewer.name"
            :value="interviewer.id"
          />
        </el-select>
      </el-form-item>
      
      <el-form-item label="面试时间" prop="interview_time">
        <el-date-picker
          v-model="form.interview_time"
          type="datetime"
          placeholder="选择面试时间"
          format="YYYY-MM-DD HH:mm"
          value-format="YYYY-MM-DDTHH:mm:ss"
          name="interview_time"
        />
      </el-form-item>
      
      <el-form-item>
        <el-button
          type="primary"
          @click.prevent="handleSubmit"
          class="confirm-schedule-btn"
          :loading="submitting"
          :disabled="submitting"
        >
          {{ submitting ? '提交中...' : '确认安排' }}
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { defineComponent, ref, reactive, onMounted, getCurrentInstance } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

export default defineComponent({
  name: 'InterviewSchedule',
  setup() {
    const { proxy } = getCurrentInstance()
    const route = useRoute()
    const router = useRouter()
    const formRef = ref(null)
    const submitting = ref(false)
    
    // 模拟数据
    const resumes = ref([
      { id: 1, name: '张三', candidate_name: '张三' },
      { id: 2, name: '李四', candidate_name: '李四' },
      { id: 3, name: '王五', candidate_name: '王五' }
    ])
    
    const jobs = ref([
      { id: 1, title: '前端开发工程师', position_name: '前端开发工程师' },
      { id: 2, title: '后端开发工程师', position_name: '后端开发工程师' },
      { id: 3, title: '产品经理', position_name: '产品经理' }
    ])
    
    const interviewers = ref([
      { id: 1, name: '张面试官', username: '张面试官' },
      { id: 2, name: '李面试官', username: '李面试官' },
      { id: 3, name: '王面试官', username: '王面试官' }
    ])
    
    // 初始化表单数据
    const form = reactive({
      resume_id: route.query.resumeId || '',
      job_requirement_id: route.query.jobId || '',
      interviewer_id: '',
      interview_time: ''
    })
    
    // 表单验证规则
    const rules = {
      resume_id: [{ required: true, message: '请选择候选人', trigger: 'change' }],
      job_requirement_id: [{ required: true, message: '请选择职位', trigger: 'change' }],
      interviewer_id: [{ required: true, message: '请选择面试官', trigger: 'change' }],
      interview_time: [{ required: true, message: '请选择面试时间', trigger: 'change' }]
    }
    
    // 获取简历列表
    const fetchResumes = async () => {
      try {
        console.log('开始获取简历列表')
        const response = await proxy.$http.resumes.getAll()
        if (response.data && response.data.resumes && response.data.resumes.length > 0) {
          resumes.value = response.data.resumes
        }
        console.log('获取到简历列表:', resumes.value)
      } catch (error) {
        console.error('获取候选人列表失败:', error)
        ElMessage.warning('使用默认候选人数据')
        // 使用默认模拟数据
      }
    }
    
    // 获取职位列表
    const fetchJobs = async () => {
      try {
        console.log('开始获取职位列表')
        const response = await proxy.$http.jobs.getAll()
        if (response.data && response.data.jobs && response.data.jobs.length > 0) {
          jobs.value = response.data.jobs
        }
        console.log('获取到职位列表:', jobs.value)
      } catch (error) {
        console.error('获取职位列表失败:', error)
        ElMessage.warning('使用默认职位数据')
        // 使用默认模拟数据
      }
    }
    
    // 获取面试官列表
    const fetchInterviewers = async () => {
      try {
        console.log('开始获取面试官列表')
        const response = await fetch('/api/v1/users?role=interviewer')
        const data = await response.json()
        if (data && data.users && data.users.length > 0) {
          interviewers.value = data.users
        }
        console.log('获取到面试官列表:', interviewers.value)
      } catch (error) {
        console.error('获取面试官列表失败:', error)
        ElMessage.warning('使用默认面试官数据')
        // 使用默认模拟数据
      }
    }
    
    // 处理表单提交
    const handleSubmit = () => {
      console.log('提交按钮被点击')
      console.log('表单数据:', form)
      
      if (!formRef.value) {
        console.error('表单引用不存在')
        ElMessage.error('表单引用不存在')
        return
      }
      
      formRef.value.validate((valid) => {
        console.log('表单验证结果:', valid)
        
        if (valid) {
          submitForm()
        } else {
          console.warn('表单验证失败')
          ElMessage.warning('请完成所有必填项')
          return false
        }
      })
    }
    
    // 提交表单
    const submitForm = async () => {
      submitting.value = true
      console.log('开始提交表单数据')
      
      try {
        const response = await proxy.$http.interviews.schedule(form)
        console.log('表单提交成功:', response.data)
        ElMessage.success('面试安排成功')
        
        // 延迟跳转，确保消息显示
        setTimeout(() => {
          router.push('/interviews')
        }, 1000)
      } catch (error) {
        console.error('表单提交失败:', error)
        ElMessage.error(error?.response?.data?.detail || '面试安排失败')
      } finally {
        submitting.value = false
      }
    }
    
    onMounted(() => {
      console.log('组件已挂载')
      fetchResumes()
      fetchJobs()
      fetchInterviewers()
    })
    
    return {
      formRef,
      form,
      rules,
      resumes,
      jobs,
      interviewers,
      submitting,
      handleSubmit
    }
  }
})
</script>

<style scoped>
.interview-schedule {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.el-select {
  width: 100%;
}
</style>
