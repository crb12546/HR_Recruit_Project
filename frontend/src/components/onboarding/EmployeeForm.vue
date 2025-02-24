<template>
  <div class="employee-form">
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="120px"
      class="employee-form"
    >
      <el-form-item label="姓名" prop="name">
        <el-input v-model="form.name" placeholder="请输入员工姓名" />
      </el-form-item>
      
      <el-form-item label="部门" prop="department">
        <el-input v-model="form.department" placeholder="请输入所属部门" />
      </el-form-item>
      
      <el-form-item label="职位" prop="position">
        <el-input v-model="form.position" placeholder="请输入职位" />
      </el-form-item>
      
      <el-form-item label="入职日期" prop="entry_date">
        <el-date-picker
          v-model="form.entry_date"
          type="date"
          placeholder="选择入职日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="submitForm">提交</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import request from '@/utils/request'

const router = useRouter()
const formRef = ref<FormInstance>()

const form = reactive({
  name: '',
  department: '',
  position: '',
  entry_date: ''
})

const rules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入员工姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  department: [
    { required: true, message: '请输入所属部门', trigger: 'blur' }
  ],
  position: [
    { required: true, message: '请输入职位', trigger: 'blur' }
  ],
  entry_date: [
    { required: true, message: '请选择入职日期', trigger: 'change' }
  ]
})

const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const response = await request.post('/api/v1/employees', form)
        ElMessage.success('员工信息创建成功')
        router.push('/employees')
      } catch (error) {
        ElMessage.error('创建失败，请重试')
      }
    }
  })
}

const resetForm = () => {
  if (!formRef.value) return
  formRef.value.resetFields()
}
</script>

<style scoped>
.employee-form {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 4px;
}
</style>
