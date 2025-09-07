<template>
	<main class="flex-grow flex flex-col gap-2 items-center justify-between">
		<section class="flex flex-col w-full">
			<h2 class="font-semibold">
				E aí, Joneta!
			</h2>

			<p>Vamos controlar os gastos juntos.</p>
		</section>

		<section class="flex flex-col gap-5 w-full">
			<TotalSpentSection
				:data="totalSpentData"
				:loading="totalSpentLoading"
			/>

			<CategoriesSection
				:categories="categories"
				:loading="categoriesLoading"
			/>
		</section>


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
				<TransactionForm
					@close="close"
					@completed="handleCompletedTransaction"
				/>
			</template>
		</UModal>
	</main>
</template>

<script setup>
import { onMounted } from 'vue';
import TransactionForm from '@/js/features/dashboard/components/TransactionForm.vue'
import { useApi } from '@/js/shared/composables/useApi'
import { getCategories, getTotalSpent } from '@/js/features/dashboard/services/dashboard'
import CategoriesSection from '@/js/features/dashboard/components/CategoriesSection.vue'
import TotalSpentSection from '@/js/features/dashboard/components/TotalSpentSection.vue'

const toast = useToast()

const {
	request: getCategoriesRequest,
	data: categories,
	loading: categoriesLoading,
} = useApi(getCategories)

const {
	request: getTotalSpentRequest,
	data: totalSpentData,
	loading: totalSpentLoading,
} = useApi(getTotalSpent)

onMounted(async () => {
	try {
		await getCategoriesRequest()
		await getTotalSpentRequest()
	} catch {
		toast.add({
			title: 'Erro ao buscar dados',
			description: 'Tente novamente mais tarde.',
			color: 'error',
		})
	}
})

async function handleCompletedTransaction() {
	console.log('entrei e vou chamar')
	await getCategoriesRequest()
}

</script>
