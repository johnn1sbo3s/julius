import api from '@/plugins/axios'
import { decodeJWT } from '@/utils/decodeToken'

export async function getCategories() {
	const token = localStorage.getItem('token')
	const userId = decodeJWT(token).sub
	console.log(userId)

	return api.get('/categories', {
		params: { user_id: userId },
	})
}