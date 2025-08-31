import api from '@/plugins/axios'
import { decodeJWT } from '@/utils/decodeToken'

export async function getCategories() {
	const token = localStorage.getItem('token')
	const userId = decodeJWT(token).sub

	return api.get('/categories', {
		params: { user_id: userId },
	})
}