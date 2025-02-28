<template>
  <div class="onboarding-form">
    <h2>{{ isEdit ? '更新入职记录' : '创建入职记录' }}</h2>
    
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
          :disabled="isEdit"
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
          :disabled="isEdit"
        >
          <el-option
            v-for="job in jobs"
            :key="job.id"
            :label="job.position_name"
            :value="job.id"
          />
        </el-select>
      </el-form-item>
      
      <el-form-item label="部门" prop="department">
        <el-input v-model="form.department" placeholder="请输入部门名称" />
      </el-form-item>
      
      <el-form-item label="职位名称" prop="position">
        <el-input v-model="form.position" placeholder="请输入具体职位名称" />
      </el-form-item>
      
      <el-form-item label="薪资" prop="salary">
        <el-input v-model="form.salary" placeholder="请输入薪资信息" />
      </el-form-item>
      
      <el-form-item label="Offer日期" prop="offer_date">
        <el-date-picker
          v-model="form.offer_date"
          type="date"
          placeholder="选择Offer日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DDT00:00:00"
          name="offer_date"
        />
      </el-form-item>
      
      <el-form-item label="入职日期" prop="start_date">
        <el-date-picker
          v-model="form.start_date"
          type="date"
          placeholder="选择入职日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DDT00:00:00"
          name="start_date"
        />
      </el-form-item>
      
      <el-form-item label="试用期结束日期" prop="probation_end_date">
        <el-date-picker
          v-model="form.probation_end_date"
          type="date"
          placeholder="选择试用期结束日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DDT00:00:00"
          name="probation_end_date"
        />
      </el-form-item>
      
      <el-form-item label="状态" prop="status">
        <el-select v-model="form.status" placeholder="请选择状态">
          <el-option label="待入职" value="pending" />
          <el-option label="入职中" value="in_progress" />
          <el-option label="已入职" value="completed" />
          <el-option label="已取消" value="cancelled" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="备注" prop="notes">
        <el-input
          v-model="form.notes"
          type="textarea"
          rows="4"
          placeholder="请输入备注信息"
        />
      </el-form-item>
      
      <el-form-item>
        <el-button
          type="primary"
          @click="submitForm"
          class="submit-btn"
        >
          {{ isEdit ? '更新' : '创建' }}
        </el-button>
        <el-button @click="goBack">取消</el-button>
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
const resumes = ref([])
const jobs = ref([])

// 判断是否为编辑模式
const isEdit = computed(() => route.params.id !== undefined)

// 初始化表单数据
const form = reactive({
  resume_id: '',
  job_requirement_id: '',
  department: '',
  position: '',
  salary: '',
  offer_date: '',
  start_date: '',
  probation_end_date: '',
  status: 'pending',
  notes: '',
  generate_tasks: true
})

// 表单验证规则
const rules = {
  resume_id: [{ required: true, message: '请选择候选人', trigger: 'change' }],
  job_requirement_id: [{ required: true, message: '请选择职位', trigger: 'change' }],
  department: [{ required: true, message: '请输入部门名称', trigger: 'blur' }],
  position: [{ required: true, message: '请输入职位名称', trigger: 'blur' }],
  offer_date: [{ required: true, message: '请选择Offer日期', trigger: 'change' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
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
    
    // 测试环境使用模拟数据
    resumes.value = [
      { id: 1, candidate_name: '张三' },
      { id: 2, candidate_name: '李四' },
      { id: 3, candidate_name: '王五' }
    ]
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
    
    // 测试环境使用模拟数据
    jobs.value = [
      { id: 1, position_name: 'Python高级工程师' },
      { id: 2, position_name: '前端开发工程师' },
      { id: 3, position_name: '产品经理' }
    ]
  }
}

// 获取入职记录详情
const fetchOnboardingDetail = async (id) => {
  try {
    const response = await fetch(`/api/v1/onboardings/${id}`)
    if (!response.ok) {
      throw new Error('获取入职记录失败')
    }
    
    const data = await response.json()
    
    // 更新表单数据
    Object.keys(form).forEach(key => {
      if (key in data) {
        form[key] = data[key]
      }
    })
  } catch (error) {
    ElMessage.error('获取入职记录失败')
    console.error('获取入职记录失败:', error)
    router.push('/onboardings')
  }
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const url = isEdit.value 
          ? `/api/v1/onboardings/${route.params.id}` 
          : '/api/v1/onboardings'
        
        const method = isEdit.value ? 'PUT' : 'POST'
        
        const response = await fetch(url, {
          method,
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(form)
        })
        
        if (response.ok) {
          ElMessage.success(isEdit.value ? '更新入职记录成功' : '创建入职记录成功')
          router.push('/onboardings')
        } else {
          const error = await response.json()
          throw new Error(error.detail || (isEdit.value ? '更新入职记录失败' : '创建入职记录失败'))
        }
      } catch (error) {
        ElMessage.error(error.message || (isEdit.value ? '更新入职记录失败' : '创建入职记录失败'))
        console.error(isEdit.value ? '更新入职记录失败:' : '创建入职记录失败:', error)
      }
    }
  })
}

// 返回列表页
const goBack = () => {
  router.push('/onboardings')
}

onMounted(() => {
  fetchResumes()
  fetchJobs()
  
  // 如果是编辑模式，获取入职记录详情
  if (isEdit.value) {
    fetchOnboardingDetail(route.params.id)
  }
})
</script>

<style scoped>
.onboarding-form {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.el-select {
  width: 100%;
}
</style>
