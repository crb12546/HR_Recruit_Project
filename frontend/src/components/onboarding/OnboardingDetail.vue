<template>
  <div class="onboarding-detail">
    <div class="onboarding-header">
      <h2>入职详情</h2>
      <div class="header-actions">
        <el-button @click="goBack">返回列表</el-button>
        <el-button type="primary" @click="editOnboarding">编辑</el-button>
      </div>
    </div>
    
    <el-card v-loading="loading" class="info-card">
      <template #header>
        <div class="card-header">
          <span>基本信息</span>
          <el-tag :type="getStatusType(onboarding.status)">
            {{ getStatusText(onboarding.status) }}
          </el-tag>
        </div>
      </template>
      
      <div class="info-item">
        <span class="label">候选人：</span>
        <span>{{ candidateName }}</span>
      </div>
      
      <div class="info-item">
        <span class="label">职位：</span>
        <span>{{ positionName }}</span>
      </div>
      
      <div class="info-item">
        <span class="label">部门：</span>
        <span>{{ onboarding.department || '未设置' }}</span>
      </div>
      
      <div class="info-item">
        <span class="label">职位名称：</span>
        <span>{{ onboarding.position || '未设置' }}</span>
      </div>
      
      <div class="info-item">
        <span class="label">薪资：</span>
        <span>{{ onboarding.salary || '未设置' }}</span>
      </div>
      
      <div class="info-item">
        <span class="label">Offer日期：</span>
        <span>{{ formatDate(onboarding.offer_date) }}</span>
      </div>
      
      <div class="info-item">
        <span class="label">入职日期：</span>
        <span>{{ formatDate(onboarding.start_date) }}</span>
      </div>
      
      <div class="info-item">
        <span class="label">试用期结束日期：</span>
        <span>{{ formatDate(onboarding.probation_end_date) }}</span>
      </div>
      
      <div class="info-item">
        <span class="label">备注：</span>
        <p class="notes">{{ onboarding.notes || '无' }}</p>
      </div>
    </el-card>
    
    <el-card class="tasks-card">
      <template #header>
        <div class="card-header">
          <span>入职任务</span>
          <el-button size="small" type="primary" @click="addTask">添加任务</el-button>
        </div>
      </template>
      
      <el-table :data="tasks" style="width: 100%">
        <el-table-column prop="name" label="任务名称" width="180" />
        <el-table-column prop="description" label="任务描述" />
        <el-table-column prop="deadline" label="截止日期" width="120">
          <template #default="scope">
            {{ formatDate(scope.row.deadline) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getTaskStatusType(scope.row.status)">
              {{ getTaskStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button
              size="small"
              @click="updateTaskStatus(scope.row.id, scope.row.status === 'completed' ? 'pending' : 'completed')"
            >
              {{ scope.row.status === 'completed' ? '标记未完成' : '标记完成' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div v-if="tasks.length === 0" class="no-tasks">
        <el-empty description="暂无入职任务" />
      </div>
    </el-card>
    
    <!-- 添加任务对话框 -->
    <el-dialog
      v-model="taskDialogVisible"
      title="添加入职任务"
      width="500px"
    >
      <el-form
        ref="taskFormRef"
        :model="taskForm"
        :rules="taskRules"
        label-width="100px"
      >
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="taskForm.name" placeholder="请输入任务名称" />
        </el-form-item>
        
        <el-form-item label="任务描述" prop="description">
          <el-input
            v-model="taskForm.description"
            type="textarea"
            rows="3"
            placeholder="请输入任务描述"
          />
        </el-form-item>
        
        <el-form-item label="截止日期" prop="deadline">
          <el-date-picker
            v-model="taskForm.deadline"
            type="date"
            placeholder="选择截止日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DDT00:00:00"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="taskDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitTaskForm">确认</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const onboarding = ref({})
const tasks = ref([])
const candidateName = ref('')
const positionName = ref('')

// 任务对话框
const taskDialogVisible = ref(false)
const taskFormRef = ref()
const taskForm = reactive({
  name: '',
  description: '',
  deadline: '',
  status: 'pending'
})

// 任务表单验证规则
const taskRules = {
  name: [{ required: true, message: '请输入任务名称', trigger: 'blur' }]
}

// 获取入职记录详情
const fetchOnboardingDetail = async () => {
  loading.value = true
  try {
    const response = await fetch(`/api/v1/onboardings/${route.params.id}`)
    if (!response.ok) {
      throw new Error('获取入职记录失败')
    }
    
    const data = await response.json()
    onboarding.value = data
    tasks.value = data.tasks || []
    
    // 获取候选人姓名
    try {
      const resumeResponse = await fetch(`/api/v1/resumes/${data.resume_id}`)
      if (resumeResponse.ok) {
        const resumeData = await resumeResponse.json()
        candidateName.value = resumeData.candidate_name
      }
    } catch (error) {
      console.error('获取候选人信息失败:', error)
      candidateName.value = '未知候选人'
    }
    
    // 获取职位名称
    try {
      const jobResponse = await fetch(`/api/v1/jobs/${data.job_requirement_id}`)
      if (jobResponse.ok) {
        const jobData = await jobResponse.json()
        positionName.value = jobData.position_name
      }
    } catch (error) {
      console.error('获取职位信息失败:', error)
      positionName.value = '未知职位'
    }
  } catch (error) {
    ElMessage.error('获取入职记录失败')
    console.error('获取入职记录失败:', error)
    router.push('/onboardings')
  } finally {
    loading.value = false
  }
}

// 返回列表页
const goBack = () => {
  router.push('/onboardings')
}

// 编辑入职记录
const editOnboarding = () => {
  router.push(`/onboardings/${route.params.id}/edit`)
}

// 添加任务
const addTask = () => {
  taskForm.name = ''
  taskForm.description = ''
  taskForm.deadline = ''
  taskForm.status = 'pending'
  taskDialogVisible.value = true
}

// 提交任务表单
const submitTaskForm = async () => {
  if (!taskFormRef.value) return
  
  await taskFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const response = await fetch(`/api/v1/onboardings/${route.params.id}/tasks`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(taskForm)
        })
        
        if (response.ok) {
          ElMessage.success('添加任务成功')
          taskDialogVisible.value = false
          fetchOnboardingDetail()
        } else {
          const error = await response.json()
          throw new Error(error.detail || '添加任务失败')
        }
      } catch (error) {
        ElMessage.error(error.message || '添加任务失败')
        console.error('添加任务失败:', error)
      }
    }
  })
}

// 更新任务状态
const updateTaskStatus = async (taskId, status) => {
  try {
    const response = await fetch(`/api/v1/onboardings/tasks/${taskId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ status })
    })
    
    if (response.ok) {
      ElMessage.success('更新任务状态成功')
      fetchOnboardingDetail()
    } else {
      const error = await response.json()
      throw new Error(error.detail || '更新任务状态失败')
    }
  } catch (error) {
    ElMessage.error(error.message || '更新任务状态失败')
    console.error('更新任务状态失败:', error)
  }
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return '未设置'
  const date = new Date(dateStr)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
}

// 获取状态类型
const getStatusType = (status) => {
  const statusMap = {
    pending: 'info',
    in_progress: 'warning',
    completed: 'success',
    cancelled: 'danger'
  }
  return statusMap[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    pending: '待入职',
    in_progress: '入职中',
    completed: '已入职',
    cancelled: '已取消'
  }
  return statusMap[status] || '未知状态'
}

// 获取任务状态类型
const getTaskStatusType = (status) => {
  const statusMap = {
    pending: 'info',
    in_progress: 'warning',
    completed: 'success',
    cancelled: 'danger'
  }
  return statusMap[status] || 'info'
}

// 获取任务状态文本
const getTaskStatusText = (status) => {
  const statusMap = {
    pending: '待完成',
    in_progress: '进行中',
    completed: '已完成',
    cancelled: '已取消'
  }
  return statusMap[status] || '未知状态'
}

onMounted(() => {
  fetchOnboardingDetail()
})
</script>

<style scoped>
.onboarding-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.onboarding-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.info-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-item {
  margin-bottom: 10px;
  line-height: 1.5;
}

.label {
  font-weight: bold;
  margin-right: 10px;
  display: inline-block;
  width: 120px;
}

.notes {
  white-space: pre-line;
  margin-top: 5px;
}

.tasks-card {
  margin-top: 20px;
}

.no-tasks {
  margin-top: 20px;
  text-align: center;
}
</style>
