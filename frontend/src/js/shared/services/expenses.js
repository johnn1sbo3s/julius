import api from '@/plugins/axios'

export async function getExpenses({ categoryId }) {
	return api.get('/expenses', { params: { category_id: categoryId } })
}