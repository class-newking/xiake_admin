<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>UserInfo表单</span>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="formData"
        :rules="rules"
        label-width="120px"
      >

        <el-form-item label="用户名" prop="username">

          <el-input v-model="formData.username" />

        </el-form-item>

        <el-form-item label="邮箱地址" prop="email">

          <el-input v-model="formData.email" />

        </el-form-item>

        <el-form-item label="年龄" prop="age">

          <el-input v-model="formData.age" />

        </el-form-item>

        <el-form-item label="是否激活" prop="is_active">

          <el-switch v-model="formData.is_active" />

        </el-form-item>

        <el-form-item label="创建时间" prop="created_at">

          <el-date-picker
            v-model="formData.created_at"
            type="datetime"
            placeholder="选择日期时间"
            format="YYYY-MM-DD HH:mm:ss"
          />

        </el-form-item>

        <el-form-item label="更新时间" prop="updated_at">

          <el-date-picker
            v-model="formData.updated_at"
            type="datetime"
            placeholder="选择日期时间"
            format="YYYY-MM-DD HH:mm:ss"
          />

        </el-form-item>

        <el-form-item label="个人简介" prop="bio">

          <el-input v-model="formData.bio" type="textarea" />

        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm">保存</el-button>
          <el-button @click="resetForm">重置</el-button>
          <el-button @click="goBack">返回</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '@/utils/api'

const route = useRoute()
const router = useRouter()
const formRef = ref()

const formData = reactive({

  username: '',

  email: '',

  age: 0,

  is_active: false,

  created_at: '',

  updated_at: '',

  bio: '',

})

const rules = {

  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],

  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' }
  ],

  age: [
    { required: false, message: '请输入年龄', trigger: 'blur' }
  ],

  is_active: [
    { required: true, message: '请输入是否激活', trigger: 'blur' }
  ],

  created_at: [
    { required: false, message: '请输入创建时间', trigger: 'blur' }
  ],

  updated_at: [
    { required: false, message: '请输入更新时间', trigger: 'blur' }
  ],

  bio: [
    { required: false, message: '请输入个人简介', trigger: 'blur' }
  ],

}

// 获取详情
const fetchDetail = async (id) => {
  try {
    const res = await api.get(`/api/userinfo/${id}/`)
    Object.assign(formData, res.data)
  } catch (err) {
    ElMessage.error('获取详情失败')
  }
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (route.params.id) {
          // 更新
          await api.put(`/api/userinfo/${route.params.id}/`, formData)
          ElMessage.success('更新成功')
        } else {
          // 创建
          await api.post('/api/userinfo/', formData)
          ElMessage.success('创建成功')
        }
        goBack()
      } catch (err) {
        ElMessage.error('操作失败')
      }
    }
  })
}

// 重置表单
const resetForm = () => {
  formRef.value.resetFields()
}

// 返回
const goBack = () => {
  router.go(-1)
}

onMounted(() => {
  if (route.params.id) {
    fetchDetail(route.params.id)
  }
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>