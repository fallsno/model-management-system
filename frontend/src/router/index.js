import { createRouter, createWebHistory } from 'vue-router'
import FamilyList from '../views/FamilyList.vue'
import VersionManage from '../views/VersionManage.vue'
import SearchResult from '../views/SearchResult.vue'
import ProductTypes from '../views/ProductTypes.vue'
import FormulaLibrary from '../views/FormulaLibrary.vue'
import DesignPointCompare from '../views/DesignPointCompare.vue'

const routes = [
  { path: '/', redirect: '/families' },
  { path: '/families', component: FamilyList, name: 'Families' },
  { path: '/families/:familyId/versions', component: VersionManage, name: 'Versions', props: true },
  { path: '/search', component: SearchResult, name: 'Search' },
  { path: '/product-types', component: ProductTypes, name: 'ProductTypes' },
  { path: '/formulas', component: FormulaLibrary, name: 'Formulas' },
  { path: '/compare', component: DesignPointCompare, name: 'Compare' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router