import { createRouter, createWebHistory } from 'vue-router'
import DashboardPage from '@/js/features/dashboard/pages/DashboardPage.vue'
import LoginRoutes from '@/js/features/login/routes/index'
import TransactionRoutes from '@/js/features/transaction/routes/index'
import RegisterRoutes from '@/js/features/register/routes/index'

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
		{
			path: '/logout',
			name: 'logout-page',
			component: DashboardPage,
			beforeEnter(to, from, next) {
				if (localStorage.getItem('token')) {
					localStorage.removeItem('token')
				}

				next('/login')
			},
		},

		...LoginRoutes,
		...TransactionRoutes,
		...RegisterRoutes,
	],
})

export default router
