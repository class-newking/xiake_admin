<template>
  <div class="app-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>UserInfo列表</span>
          <el-button type="primary" @click="handleCreate">新增</el-button>
        </div>
      </template>

      <el-table :data="list" border style="width: 100%">

        <el-table-column prop="id" label="ID" />

        <el-table-column prop="username" label="用户名" />

        <el-table-column prop="email" label="邮箱地址" />

        <el-table-column prop="age" label="年龄" />

        <el-table-column prop="is_active" label="是否激活" />

        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '@/utils/api'

const list = ref([])
const loading = ref(false)
const pagination = reactive({
  page: 1,
  pageSize: 10,
  total: 0
})

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const res = await api.get('/api/userinfo/', {
      params: {
        page: pagination.page,
        page_size: pagination.pageSize
      }
    })
    list.value = res.data.results
    pagination.total = res.data.count
  } catch (err) {
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

// 新增
const handleCreate = () => {
  // 跳转到新增页面
}

// 编辑
const handleEdit = (row) => {
  // 跳转到编辑页面
}

// 删除
const handleDelete = (row) => {
  ElMessageBox.confirm('确认删除该记录?', '提示', {
    confirmButtonText: '确认',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await api.delete(`/api/userinfo/${row.id}/`)
      ElMessage.success('删除成功')
      fetchData()
    } catch (err) {
      ElMessage.error('删除失败')
    }
  })
}

// 分页
const handleSizeChange = (val) => {
  pagination.pageSize = val
  fetchData()
}

const handleCurrentChange = (val) => {
  pagination.page = val
  fetchData()
}

onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>