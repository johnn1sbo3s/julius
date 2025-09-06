<template>
	<div>
		<div
			v-if="loading"
			class="flex flex-col gap-3 w-full"
		>
			<USkeleton class="w-52 h-7" />

			<div class="grid grid-cols-2 w-full gap-2">
				<USkeleton
					v-for="i in 6"
					:key="i"
					class="w-full h-18"
				/>
			</div>
		</div>

		<div
			v-else
			class="flex flex-col gap-3 w-full"
		>
			<h3 class="font-semibold">
				Gastos por categoria
			</h3>

			<div class="grid grid-cols-2 w-full gap-3">
				<UCard
					v-for="category in categories"
					:key="category.id"
					class="w-full bg-slate-800 backdrop-blur-2xl border-1 border-slate-700"
				>
					<div class="flex flex-col gap-2">
						<span class="text-sm font-semibold">
							{{ category.name }}
						</span>

						<div class="flex flex-col">
							<span class="font-bold text-lg">
								{{ formatCurrency(category.totalSpent) }}
							</span>

							<span class="text-sm">
								de {{ formatCurrency(category.budget) || 'Não definido' }}
							</span>
						</div>
					</div>
				</UCard>
			</div>
		</div>
	</div>
</template>

<script setup>
import { formatCurrency } from '@/utils/formatCurrency'

const props = defineProps({
	categories: {
		type: Array,
		required: true,
	},
	loading: {
		type: Boolean,
		required: true,
	},
})

</script>

<style lang="scss" scoped>

</style>