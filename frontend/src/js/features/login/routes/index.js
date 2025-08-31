import LoginPage from '@/js/features/login/pages/LoginPage.vue';

export default [
	{
		path: '/login',
		name: 'login-page',
		component: LoginPage,
		beforeEnter(to, from, next) {
			if (localStorage.getItem('token')) {
				next('/')
			}

			next()
		},
	},
]