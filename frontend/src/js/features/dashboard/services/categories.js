import api from '@/plugins/axios'

export async function getCategories() {
	return api.get('/dashboard/categories')
}