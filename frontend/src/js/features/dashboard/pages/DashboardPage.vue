<template>
	<main class="flex-grow flex flex-col gap-2 items-center justify-between">
		<img
			src="/img/logo.svg"
			alt="Logo"
			class="w-40 mt-6"
		>

		<h1>Dashboard</h1>

		<UModal
			title="Novo gasto"
			:dismissible="false"
		>
			<UButton
				class="w-full justify-center mb-8"
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

<script lang="ts" setup>
import TransactionForm from '@/js/features/dashboard/components/TransactionForm.vue'

</script>
