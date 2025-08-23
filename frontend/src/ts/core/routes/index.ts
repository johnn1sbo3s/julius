import { createRouter, createWebHistory } from 'vue-router'
import DashboardPage from '@/ts/features/dashboard/pages/DashboardPage.vue'
import TransactionRoutes from '@/ts/features/transaction/routes/index'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard-page',
      component: DashboardPage,
    },

    ...TransactionRoutes,
  ],
})

export default router
