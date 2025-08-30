import RegisterPage from '@/js/features/register/pages/RegisterPage.vue';

export default [
	{
		path: '/register',
		name: 'register',
		component: RegisterPage,
		beforeEnter(to, from, next) {
			if (localStorage.getItem('token')) {
				next('/')
			}

			next()
		},
	},
]