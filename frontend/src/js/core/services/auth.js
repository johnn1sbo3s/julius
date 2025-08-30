import api from '@/plugins/axios'

export async function login({ email, password }) {
	return api.post('/auth/login-json', {
		email,
		password,
	})
}

export async function register({ name, email, password }) {
	return api.post('/users/register', {
		name,
		email,
		password,
	})
}