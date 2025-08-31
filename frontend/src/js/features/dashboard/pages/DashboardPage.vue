<template>
	<main class="flex-grow flex flex-col gap-2 items-center justify-between">
		<img
			src="/img/logo.svg"
			alt="Logo"
			class="w-40 mt-6"
		>

		<h1 class="font-semibold">
			Dashboard
		</h1>

		<UModal
			title="Novo gasto"
			:dismissible="false"
		>
			<UButton
				class="w-full justify-center mb-8 cursor-pointer"
				size="xl"
				icon="i-lucide-wallet-minimal"
			>
				Nova Transação
			</UButton>

			<template #body="{ close }">
				<TransactionForm @close="close" />
			</template>
		</UModal>
	</main>
</template>

<script setup>
import TransactionForm from '@/js/features/dashboard/components/TransactionForm.vue'
import { useApi } from '@/js/shared/composables/useApi'
import { getCategories } from '@/js/features/dashboard/services/categories'
import { onMounted } from 'vue';

const { request: getCategoriesRequest, data, error, loading } = useApi(getCategories);

onMounted(async () => {
	await getCategoriesRequest()
})

</script>
