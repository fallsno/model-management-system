<template>
  <div class="version-manage">
    <el-page-header @back="$router.push('/families')">
      <template #content>
        <span>{{ family?.family_code }} {{ family?.family_name }}</span>
      </template>
    </el-page-header>

    <el-card style="margin-top: 20px">
      <template #header>
        <div class="card-header">
          <span>版本列表</span>
          <el-button type="primary" @click="showVersionDialog = true">
            <el-icon><Plus /></el-icon>新建版本
          </el-button>
        </div>
      </template>

      <el-tabs v-model="activeVersionId" type="card" @tab-click="onVersionChange">
        <el-tab-pane v-for="ver in versions" :key="ver.id" :label="ver.version_code" :name="ver.id">
          <template #label>
            <span>{{ ver.version_code }}</span>
            <el-icon class="delete-version-icon" @click.stop="deleteVersion(ver.id)">
              <Close />
            </el-icon>
          </template>
          <!-- 部件管理 -->
          <div v-if="activeVersionId === ver.id">
            <el-button type="success" @click="showPartDialog = true" style="margin-bottom: 15px">
              <el-icon><Plus /></el-icon>新增部件
            </el-button>

            <el-collapse v-model="activeParts" accordion>
              <el-collapse-item v-for="part in parts" :key="part.id" :name="part.id">
                <template #title>
                  <div style="display: flex; align-items: center; gap: 10px; width: 100%">
                    <span><strong>{{ part.part_category }}</strong> - {{ part.part_name || '未命名' }}</span>
                    <el-tag size="small">{{ part.parameters?.length || 0 }} 个参数</el-tag>
                    <el-button link type="danger" @click.stop="deletePart(part.id)">删除</el-button>
                  </div>
                </template>

                <!-- 新增 Tab 切换：参数表 / 设计流程 / 附件 -->
                <el-tabs type="border-card">
                  <el-tab-pane label="参数表">
                    <ParamTable :part-id="part.id" :parameters="part.parameters" @refresh="fetchParts" />
                  </el-tab-pane>
                  <el-tab-pane label="设计流程">
                    <DesignFlowPanel :part-id="part.id" />
                  </el-tab-pane>
                  <el-tab-pane label="附件">
                    <FileUploader :version-id="ver.id" :part-id="part.id" />
                  </el-tab-pane>
                </el-tabs>
              </el-collapse-item>
            </el-collapse>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 新建版本对话框 -->
    <el-dialog v-model="showVersionDialog" title="新建版本" width="400px">
      <el-form :model="versionForm">
        <el-form-item label="版本号" required>
          <el-input v-model="versionForm.version_code" placeholder="例如 V1.0" />
        </el-form-item>
        <el-form-item label="规格说明">
          <el-input v-model="versionForm.specification" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showVersionDialog = false">取消</el-button>
        <el-button type="primary" @click="createVersion">创建</el-button>
      </template>
    </el-dialog>

    <!-- 新增部件对话框 -->
    <el-dialog v-model="showPartDialog" title="新增部件" width="400px">
      <el-form :model="partForm">
        <el-form-item label="部件分类" required>
          <el-select v-model="partForm.part_category" placeholder="选择分类">
            <el-option label="进料端座" value="进料端座" />
            <el-option label="出料端座" value="出料端座" />
            <el-option label="托轮" value="托轮" />
            <el-option label="限位轮" value="限位轮" />
            <el-option label="传动装置" value="传动装置" />
            <el-option label="滚筒体" value="滚筒体" />
            <el-option label="其他" value="其他" />
          </el-select>
        </el-form-item>
        <el-form-item label="部件名称" required>
          <el-input v-model="partForm.part_name" placeholder="例如 前端进料座" />
        </el-form-item>
        <el-form-item label="部件编号">
          <el-input v-model="partForm.part_code" placeholder="例如 AT240R-01" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPartDialog = false">取消</el-button>
        <el-button type="primary" @click="createPart">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import ParamTable from '@/components/ParamTable.vue'
import FileUploader from '@/components/FileUploader.vue'
import DesignFlowPanel from '@/components/DesignFlowPanel.vue'   // 新增

const route = useRoute()
const familyId = ref(route.params.familyId)
const family = ref(null)
const versions = ref([])
const activeVersionId = ref(null)
const parts = ref([])
const activeParts = ref([])

const showVersionDialog = ref(false)
const showPartDialog = ref(false)
const versionForm = ref({ version_code: '', specification: '' })
const partForm = ref({ part_category: '', part_name: '', part_code: '' })

const fetchFamily = async () => {
  const res = await axios.get(`/families/${familyId.value}`)
  family.value = res.data
}

const fetchVersions = async () => {
  const res = await axios.get(`/families/${familyId.value}/versions`)
  versions.value = res.data
  if (versions.value.length > 0) {
    activeVersionId.value = versions.value[0].id
    fetchParts()
  } else {
    parts.value = []
    activeVersionId.value = null
  }
}

const fetchParts = async () => {
  if (!activeVersionId.value) return
  const res = await axios.get(`/versions/${activeVersionId.value}/parts`)
  parts.value = res.data
}

const onVersionChange = () => {
  fetchParts()
}

const createVersion = async () => {
  if (!versionForm.value.version_code?.trim()) {
    ElMessage.warning('版本号不能为空')
    return
  }
  try {
    await axios.post(`/families/${familyId.value}/versions`, versionForm.value)
    ElMessage.success('版本创建成功')
    showVersionDialog.value = false
    versionForm.value = { version_code: '', specification: '' }
    fetchVersions()
  } catch (e) {
    ElMessage.error('创建版本失败')
  }
}

const createPart = async () => {
  if (!partForm.value.part_category) {
    ElMessage.warning('请选择部件分类')
    return
  }
  if (!partForm.value.part_name?.trim()) {
    ElMessage.warning('部件名称不能为空')
    return
  }
  try {
    await axios.post(`/versions/${activeVersionId.value}/parts`, partForm.value)
    ElMessage.success('部件创建成功')
    showPartDialog.value = false
    partForm.value = { part_category: '', part_name: '', part_code: '' }
    fetchParts()
  } catch (e) {
    ElMessage.error('创建部件失败')
  }
}

const deletePart = async (partId) => {
  try {
    await axios.delete(`/versions/parts/${partId}`)
    ElMessage.success('部件已删除')
    fetchParts()
  } catch (e) {
    ElMessage.error('删除失败')
  }
}

const deleteVersion = async (versionId) => {
  await ElMessageBox.confirm('确定删除该版本及其所有部件和参数吗？', '警告', { type: 'warning' })
  try {
    await axios.delete(`/versions/${versionId}`)
    ElMessage.success('版本已删除')
    await fetchVersions()
    if (activeVersionId.value === versionId) {
      activeVersionId.value = versions.value[0]?.id || null
      fetchParts()
    }
  } catch (e) {
    ElMessage.error('删除失败')
  }
}

onMounted(async () => {
  await fetchFamily()
  await fetchVersions()
})
</script>

<style scoped>
.version-manage { padding: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.delete-version-icon {
  margin-left: 8px;
  cursor: pointer;
  vertical-align: middle;
}
.delete-version-icon:hover {
  color: #f56c6c;
}
</style>