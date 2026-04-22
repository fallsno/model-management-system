<template>
  <div class="product-types">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>产品类型管理</span>
          <el-button type="primary" @click="showDialog = true">
            <el-icon><Plus /></el-icon>新增类型
          </el-button>
        </div>
      </template>

      <el-table :data="types" v-loading="loading" stripe>
        <el-table-column prop="type_code" label="类型代码" width="150" />
        <el-table-column prop="type_name" label="类型名称" width="180" />
        <el-table-column prop="description" label="描述" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button type="primary" link @click="editType(row)">编辑</el-button>
            <el-button type="danger" link @click="deleteType(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="showDialog" :title="editing ? '编辑类型' : '新增类型'" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="类型代码" required>
          <el-input v-model="form.type_code" placeholder="例如 DRYER_DRUM" />
        </el-form-item>
        <el-form-item label="类型名称" required>
          <el-input v-model="form.type_name" placeholder="例如 干燥滚筒" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="saveType">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

const types = ref([])
const loading = ref(false)
const showDialog = ref(false)
const editing = ref(false)
const form = ref({ type_code: '', type_name: '', description: '' })
let editingId = null

const fetchTypes = async () => {
  loading.value = true
  try {
    const res = await axios.get('/product-types/')
    types.value = res.data
  } catch (e) {
    ElMessage.error('获取产品类型失败')
  } finally {
    loading.value = false
  }
}

const saveType = async () => {
  if (!form.value.type_code.trim() || !form.value.type_name.trim()) {
    ElMessage.warning('类型代码和名称不能为空')
    return
  }
  try {
    if (editing.value) {
      await axios.put(`/product-types/${editingId}`, form.value)
      ElMessage.success('更新成功')
    } else {
      await axios.post('/product-types/', form.value)
      ElMessage.success('创建成功')
    }
    showDialog.value = false
    editing.value = false
    form.value = { type_code: '', type_name: '', description: '' }
    editingId = null
    fetchTypes()
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

const editType = (row) => {
  editing.value = true
  editingId = row.id
  form.value = { ...row }
  showDialog.value = true
}

const deleteType = async (id) => {
  await ElMessageBox.confirm('确定删除该产品类型吗？', '警告', { type: 'warning' })
  try {
    await axios.delete(`/product-types/${id}`)
    ElMessage.success('删除成功')
    fetchTypes()
  } catch (e) {
    ElMessage.error('删除失败')
  }
}

onMounted(fetchTypes)
</script>

<style scoped>
.product-types { padding: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>