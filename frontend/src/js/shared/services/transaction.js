import api from '@/plugins/axios'

export async function postTransaction({ amount, description, expenseId }) {
	return api.post('/transactions', {
		amount,
		description,
		expense_id: expenseId,
	})
}