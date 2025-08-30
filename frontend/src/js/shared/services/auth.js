import api from '@/plugins/axios'

export async function login({ email, password }) {
	return api.post('/auth/login-json', {
		email,
		password,
	})
}