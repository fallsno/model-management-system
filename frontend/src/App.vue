<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h2>📋 型号版本管理系统</h2>
          <div class="header-actions">
            <SearchBar @search="handleSearch" @select="handleSelect" />
            <el-button type="default" @click="$router.push('/product-types')">
              <el-icon><Folder /></el-icon>产品类型
            </el-button>
            <el-button type="default" @click="$router.push('/formulas')">
              <el-icon><Document /></el-icon>公式库
            </el-button>
            <el-button type="default" @click="$router.push('/compare')">
              <el-icon><DataAnalysis /></el-icon>设计点对比
            </el-button>
            <el-button type="primary" @click="openMonitor">
              <el-icon><Monitor /></el-icon>滚筒监测
            </el-button>
            <el-button type="success" @click="openToolbox">
              <el-icon><Tools /></el-icon>工具箱
            </el-button>
          </div>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import SearchBar from '@/components/SearchBar.vue'

const router = useRouter()
const handleSearch = (kw) => router.push({ name: 'Search', query: { q: kw } })
const handleSelect = (item) => {
  if (item.type === 'model' && item.family_id) {
    router.push({ name: 'Versions', params: { familyId: item.family_id } })
  }
}

const openMonitor = () => window.open('/monitor', '_blank')
const openToolbox = () => window.open('http://10.30.10.64:5002', '_blank')
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Microsoft YaHei', sans-serif; background: #f0f2f5; }
.el-header { background: #1e293b; color: white; display: flex; align-items: center; padding: 0 20px; }
.header-content { width: 100%; display: flex; justify-content: space-between; align-items: center; }
.header-actions { display: flex; gap: 20px; align-items: center; }
h2 { color: #38bdf8; margin: 0; }
</style>
