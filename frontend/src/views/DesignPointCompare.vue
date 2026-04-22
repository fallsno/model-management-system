<template>
  <div class="design-point-compare">
    <el-card>
      <template #header>
        <span>设计点对比</span>
      </template>
      <el-form inline>
        <el-form-item label="设计点名称">
          <el-input v-model="designPoint" placeholder="例如 滚筒直径" style="width: 300px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="search">查询</el-button>
          <el-button @click="exportData">导出</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="results" v-loading="loading" border>
        <el-table-column prop="family_code" label="型号代号" width="150" />
        <el-table-column prop="family_name" label="型号名称" width="150" />
        <el-table-column prop="version_code" label="版本" width="120" />
        <el-table-column prop="part_name" label="部件" width="150" />
        <el-table-column prop="flow_name" label="设计流程" width="150" />
        <el-table-column prop="step_order" label="步骤编号" width="100" />
        <el-table-column label="输出参数">
          <template #default="{ row }">
            <div v-for="out in row.outputs" :key="out.name">
              {{ out.name }} = {{ out.value }} {{ out.unit }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="note" label="说明" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import * as XLSX from 'xlsx'

const designPoint = ref('')
const results = ref([])
const loading = ref(false)

const search = async () => {
  if (!designPoint.value.trim()) return
  loading.value = true
  try {
    const res = await axios.get('/compare/design-point/' + encodeURIComponent(designPoint.value))
    results.value = res.data
  } catch (e) {
    ElMessage.error('查询失败')
  } finally {
    loading.value = false
  }
}

const exportData = () => {
  const ws = XLSX.utils.json_to_sheet(results.value)
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, '对比结果')
  XLSX.writeFile(wb, `设计点对比_${designPoint.value}.xlsx`)
}
</script>