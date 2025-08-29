import { createRouter, createWebHistory } from 'vue-router'
import DashboardPage from '@/ts/features/dashboard/pages/DashboardPage.vue'
import LoginRoutes from '@/ts/features/login/routes/index'
import TransactionRoutes from '@/ts/features/transaction/routes/index'

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: '/',
			name: 'dashboard-page',
			component: DashboardPage,
			beforeEnter(to, from, next) {
				if (localStorage.getItem('token')) {
					next()
				}

				next('/login')
			},
		},

		...LoginRoutes,
		...TransactionRoutes,
	],
})

export default router
