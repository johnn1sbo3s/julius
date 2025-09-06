import axios from 'axios'
import { decodeJWT } from '../utils/decodeToken';

const api = axios.create({
	baseURL: 'http://localhost:8000/api/v1',
	timeout: 10000,
	headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
	const token = localStorage.getItem("token")

	if (token) {
		config.headers.Authorization = `Bearer ${token}`
	}

	return config
})

api.interceptors.response.use(
	(response) => response,

	async (error) => {
		const originalRequest = error.config;

		if (error.response?.status === 401) {
			try {
				const oldToken = localStorage.getItem("token");

				const refreshResponse = await axios.post(
					'http://localhost:8000/api/v1/auth/refresh',
					{},
					{ headers: { Authorization: `Bearer ${oldToken}` } }
				);

				const newToken = refreshResponse.data.token;
				localStorage.setItem("token", newToken);

				originalRequest.headers.Authorization = `Bearer ${newToken}`;
				originalRequest.headers.Authorization = `Bearer ${newToken}`;
				return api(originalRequest);

			} catch (refreshError) {
				return Promise.reject(refreshError);
			}
		}

		return Promise.reject(error);
	}
);

export default api;