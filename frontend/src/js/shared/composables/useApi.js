import { ref } from 'vue'

export function useApi(service) {
	const data = ref(null);
	const errorMsg = ref('');
	const loading = ref(false);

	async function request(...args) {
		loading.value = true;

		try {
			data.value = await service(...args);
			data.value = data.value?.data
			return data.value?.data
		} catch (error) {
			errorMsg.value = error.response?.data || error.message
			throw error
		} finally {
			loading.value = false;
		}
	}

	return {
		data,
		loading,
		error: errorMsg,
		request,
	}
}