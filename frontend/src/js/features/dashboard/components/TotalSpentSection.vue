<template>
	<div>
		<div
			v-if="loading"
			class="flex flex-col gap-3 w-full"
		>
			<USkeleton class="w-40 h-6" />

			<USkeleton class="w-full h-30" />
		</div>

		<div
			v-else
			class="flex flex-col gap-3 w-full"
		>
			<h3 class="font-semibold">
				Total gasto no mês
			</h3>

			<UCard class="w-full bg-slate-800 backdrop-blur-2xl border-1 border-slate-700">
				<div class="flex justify-between">
					<div class="flexgap-2">
						<span class="text-xl font-bold text-amber-400">
							{{ formatCurrency(data?.spent) }}
						</span>

						<span class="text-sm">
							de {{ data?.budget != 0 ? formatCurrency(data?.budget) : 'Não definido' }}
						</span>
					</div>

					<UBadge
						size="sm"
						color="warning"
						variant="soft"
					>
						{{ data?.month }}
					</UBadge>
				</div>

				<UProgress
					v-if="progressBarValue"
					v-model="progressBarValue"
					class="mt-3"
					:color="progressBarValue > 80 ? 'error' : 'primary'"
				/>

				<div
					class="flex justify-between text-xs font-semibold mt-2"
					:class="progressBarValue > 80 ? 'text-error' : ''"
				>
					<span>
						Saldo: {{ formatCurrency(data?.budget - data?.spent) }}
					</span>

					<span>
						{{ progressBarValue }}%
					</span>
				</div>
			</UCard>
		</div>
	</div>
</template>

<script setup>
import { computed } from 'vue'
import { formatCurrency } from '@/utils/formatCurrency'

const props = defineProps({
	data: {
		type: Object,
		required: true,
	},
	loading: {
		type: Boolean,
		required: true,
	},
})

const progressBarValue = computed(() => {
	const moneyLeft = props.data?.budget - props.data?.spent

	if (moneyLeft <= 0) return 100

	return (props.data?.spent / props.data?.budget) * 100
})

</script>

<style lang="scss" scoped>

</style>
