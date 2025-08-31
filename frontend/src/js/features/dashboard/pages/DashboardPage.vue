<template>
	<main class="flex-grow flex flex-col gap-2 items-center justify-between">
		<section class="flex flex-col w-full">
			<h2 class="font-semibold">
				E aí, Joneta!
			</h2>

			<p>Vamos controlar os gastos juntos.</p>
		</section>

		<section class="flex flex-col gap-4 w-full">
			<h3 class="font-semibold">
				Gastos por categoria
			</h3>

			<div class="grid grid-cols-2 w-full gap-2">
				<UCard
					v-for="category in categories"
					:key="category.id"
					class="w-full"
				>
					<div>
						Chama
					</div>
				</UCard>
			</div>
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
				<TransactionForm @close="close" />
			</template>
		</UModal>
	</main>
</template>

<script setup>
import { onMounted } from 'vue';
import TransactionForm from '@/js/features/dashboard/components/TransactionForm.vue'
import { useApi } from '@/js/shared/composables/useApi'
import { getCategories } from '@/js/features/dashboard/services/categories'

const { request: getCategoriesRequest, data: categories, error, loading } = useApi(getCategories);

onMounted(async () => {
	await getCategoriesRequest()
	console.log(categories.value)
})

</script>
