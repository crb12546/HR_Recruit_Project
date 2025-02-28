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
            :label="resume.candidate_name"
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
            :label="job.position_name"
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
            :label="interviewer.username"
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
          @click="submitForm"
          class="confirm-schedule-btn"
        >
          确认安排
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const formRef = ref()
const resumes = ref([])
const jobs = ref([])
const interviewers = ref([])

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
    const response = await fetch('/api/v1/resumes')
    const data = await response.json()
    resumes.value = data.resumes || []
  } catch (error) {
    ElMessage.error('获取候选人列表失败')
    console.error('获取候选人列表失败:', error)
  }
}

// 获取职位列表
const fetchJobs = async () => {
  try {
    const response = await fetch('/api/v1/jobs')
    const data = await response.json()
    jobs.value = data.jobs || []
  } catch (error) {
    ElMessage.error('获取职位列表失败')
    console.error('获取职位列表失败:', error)
  }
}

// 获取面试官列表
const fetchInterviewers = async () => {
  try {
    const response = await fetch('/api/v1/users?role=interviewer')
    const data = await response.json()
    interviewers.value = data.users || []
  } catch (error) {
    ElMessage.error('获取面试官列表失败')
    console.error('获取面试官列表失败:', error)
    
    // 测试环境使用模拟数据
    interviewers.value = [
      { id: 1, username: '张面试官' },
      { id: 2, username: '李面试官' },
      { id: 3, username: '王面试官' }
    ]
  }
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const response = await fetch('/api/v1/interviews', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(form)
        })
        
        if (response.ok) {
          ElMessage.success('面试安排成功')
          router.push('/interviews')
        } else {
          const error = await response.json()
          throw new Error(error.detail || '面试安排失败')
        }
      } catch (error) {
        ElMessage.error(error.message || '面试安排失败')
        console.error('面试安排失败:', error)
      }
    }
  })
}

onMounted(() => {
  fetchResumes()
  fetchJobs()
  fetchInterviewers()
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
