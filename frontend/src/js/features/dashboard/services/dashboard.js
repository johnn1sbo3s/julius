import api from '@/plugins/axios'

export async function getCategories() {
	return api.get('/dashboard/categories')
}

export async function getTotalSpent() {
	return api.get('/dashboard/total-spent')
}
