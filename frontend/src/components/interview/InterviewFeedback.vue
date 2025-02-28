<template>
  <div class="interview-feedback" v-loading="loading">
    <h2>面试反馈</h2>
    
    <div v-if="interview" class="interview-info">
      <el-descriptions title="面试信息" :column="1" border>
        <el-descriptions-item label="候选人">{{ candidateName }}</el-descriptions-item>
        <el-descriptions-item label="职位">{{ positionName }}</el-descriptions-item>
        <el-descriptions-item label="面试官">{{ interviewerName }}</el-descriptions-item>
        <el-descriptions-item label="面试时间">{{ formatDateTime(interview.interview_time) }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(interview.status)">
            {{ getStatusText(interview.status) }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </div>
    
    <div v-if="questions.length > 0" class="interview-questions">
      <h3>面试问题</h3>
      <el-collapse>
        <el-collapse-item
          v-for="(question, index) in questions"
          :key="index"
          :title="`问题 ${index + 1}: ${question.content}`"
          :name="index"
        >
          <div class="question-type">类型: {{ question.type }}</div>
        </el-collapse-item>
      </el-collapse>
    </div>
    
    <el-divider />
    
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      class="feedback-form"
    >
      <el-form-item label="评分" prop="score">
        <el-rate
          v-model="form.score"
          :max="5"
          :colors="['#F56C6C', '#E6A23C', '#67C23A']"
          :texts="['不合适', '待考虑', '一般', '良好', '优秀']"
          show-text
        />
      </el-form-item>
      
      <el-form-item label="反馈意见" prop="feedback">
        <el-input
          v-model="form.feedback"
          type="textarea"
          :rows="4"
          placeholder="请输入面试反馈意见"
        />
      </el-form-item>
      
      <el-form-item label="面试结果" prop="status">
        <el-radio-group v-model="form.status">
          <el-radio label="completed">通过</el-radio>
          <el-radio label="rejected">不通过</el-radio>
          <el-radio label="pending">待定</el-radio>
        </el-radio-group>
      </el-form-item>
      
      <el-form-item>
        <el-button
          type="primary"
          @click="submitForm"
        >
          提交反馈
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const formRef = ref()
const loading = ref(false)
const interview = ref(null)
const questions = ref([])
const candidateName = ref('')
const positionName = ref('')
const interviewerName = ref('')

// 初始化表单数据
const form = reactive({
  score: 3,
  feedback: '',
  status: 'completed'
})

// 表单验证规则
const rules = {
  score: [{ required: true, message: '请评分', trigger: 'change' }],
  feedback: [{ required: true, message: '请输入反馈意见', trigger: 'blur' }],
  status: [{ required: true, message: '请选择面试结果', trigger: 'change' }]
}

// 获取面试详情
const fetchInterviewDetail = async () => {
  const interviewId = route.params.id
  if (!interviewId) return
  
  loading.value = true
  try {
    const response = await fetch(`/api/v1/interviews/${interviewId}`)
    if (response.ok) {
      interview.value = await response.json()
      
      // 获取关联数据
      await Promise.all([
        fetchResume(interview.value.resume_id),
        fetchJob(interview.value.job_requirement_id),
        fetchInterviewer(interview.value.interviewer_id)
      ])
      
      // 生成面试问题
      await generateQuestions(interviewId)
    } else {
      ElMessage.error('获取面试详情失败')
    }
  } catch (error) {
    ElMessage.error('获取面试详情失败')
    console.error('获取面试详情失败:', error)
  } finally {
    loading.value = false
  }
}

// 获取简历信息
const fetchResume = async (resumeId) => {
  try {
    const response = await fetch(`/api/v1/resumes/${resumeId}`)
    if (response.ok) {
      const resume = await response.json()
      candidateName.value = resume.candidate_name
    }
  } catch (error) {
    console.error('获取简历信息失败:', error)
    candidateName.value = '未知候选人'
  }
}

// 获取职位信息
const fetchJob = async (jobId) => {
  try {
    const response = await fetch(`/api/v1/jobs/${jobId}`)
    if (response.ok) {
      const job = await response.json()
      positionName.value = job.position_name
    }
  } catch (error) {
    console.error('获取职位信息失败:', error)
    positionName.value = '未知职位'
  }
}

// 获取面试官信息
const fetchInterviewer = async (interviewerId) => {
  try {
    const response = await fetch(`/api/v1/users/${interviewerId}`)
    if (response.ok) {
      const interviewer = await response.json()
      interviewerName.value = interviewer.username
    }
  } catch (error) {
    console.error('获取面试官信息失败:', error)
    interviewerName.value = '未知面试官'
  }
}

// 生成面试问题
const generateQuestions = async (interviewId) => {
  try {
    const response = await fetch(`/api/v1/interviews/${interviewId}/questions`, {
      method: 'POST'
    })
    if (response.ok) {
      const data = await response.json()
      questions.value = data.questions || []
    }
  } catch (error) {
    console.error('生成面试问题失败:', error)
  }
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      const interviewId = route.params.id
      if (!interviewId) return
      
      try {
        const response = await fetch(`/api/v1/interviews/${interviewId}/feedback`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(form)
        })
        
        if (response.ok) {
          ElMessage.success('面试反馈提交成功')
          router.push('/interviews')
        } else {
          const error = await response.json()
          throw new Error(error.detail || '面试反馈提交失败')
        }
      } catch (error) {
        ElMessage.error(error.message || '面试反馈提交失败')
        console.error('面试反馈提交失败:', error)
      }
    }
  })
}

// 格式化日期时间
const formatDateTime = (dateTimeStr) => {
  if (!dateTimeStr) return '未设置'
  const date = new Date(dateTimeStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

// 获取状态类型
const getStatusType = (status) => {
  const statusMap = {
    scheduled: 'info',
    completed: 'success',
    rejected: 'danger',
    pending: 'warning',
    cancelled: 'info'
  }
  return statusMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    scheduled: '待面试',
    completed: '已通过',
    rejected: '未通过',
    pending: '待定',
    cancelled: '已取消'
  }
  return statusMap[status] || '未知状态'
}

onMounted(() => {
  fetchInterviewDetail()
})
</script>

<style scoped>
.interview-feedback {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.interview-info {
  margin-bottom: 20px;
}

.interview-questions {
  margin: 20px 0;
}

.question-type {
  color: #909399;
  font-size: 14px;
  margin-top: 5px;
}

.feedback-form {
  margin-top: 20px;
}
</style>
