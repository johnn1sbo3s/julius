<template>
	<div>
		<UForm
			class="flex flex-col gap-4"
			:state="state"
			:schema="schema"
			@submit="handleSubmit"
		>
			<UFormField
				label="Valor"
				name="amount"
				required
			>
				<UInput
					v-model="state.amount"
					class="w-full"
					size="xl"
					type="number"
				/>
			</UFormField>

			<UFormField
				label="Categoria"
				name="category"
				required
			>
				<USelect
					v-model="state.category"
					class="w-full"
					size="xl"
					type="text"
					:items="categoriesOptions"
					:loading="categoriesLoading"
				/>
			</UFormField>

			<UFormField
				label="Gasto"
				name="expense"
				required
			>
				<USelect
					v-model="state.expense"
					class="w-full"
					size="xl"
					type="text"
					:items="expensesOptions"
					:disabled="!state.category"
					:loading="expensesLoading"
				/>
			</UFormField>

			<UFormField
				label="Descrição"
				name="description"
			>
				<UInput
					v-model="state.description"
					class="w-full"
					size="xl"
					type="text"
				/>
			</UFormField>

			<div class="flex gap-2">
				<UButton
					class="w-full justify-center cursor-pointer"
					size="xl"
					color="neutral"
					@click="handleCancelClick"
				>
					Cancelar
				</UButton>

				<UButton
					class="w-full justify-center cursor-pointer"
					size="xl"
					type="submit"
					:loading="postTransactionLoading"
				>
					Confirmar
				</UButton>
			</div>
		</UForm>
	</div>
</template>

<script setup>
import { onMounted, reactive, computed, watch, watchEffect } from 'vue'
import * as v from 'valibot'
import { getCategories } from '@/js/shared/services/categories'
import { getExpenses } from '@/js/shared/services/expenses'
import { postTransaction } from '@/js/shared/services/transaction'
import { useApi } from '@/js/shared/composables/useApi'

const { toast } = useToast()

const emits = defineEmits(['close', 'completed']);

const {
	request: categoriesRequest,
	data: categoriesData,
	loading: categoriesLoading,
	error: categoriesError,
} = useApi(getCategories)

const {
	request: expensesRequest,
	data: expensesData,
	loading: expensesLoading,
	error: expensesError,
} = useApi(getExpenses)

const {
	request: postTransactionRequest,
	loading: postTransactionLoading,
} = useApi(postTransaction)

const state = reactive({
	amount: null,
	category: null,
	expense: null,
	description: '',
});

const schema = v.object({
	amount: v.pipe(
		v.number('O valor deve ser um número.'),
		v.minValue(1, 'O valor deve ser maior que zero.'),
	),
	category: v.number('Selecione uma categoria.'),
	expense: v.number('Selecione um gasto.'),
	description: v.string('Insira uma descrição válida.'),
});

const categoriesOptions = computed(() => {
	if (!categoriesData.value) return []

	return categoriesData.value.map((item) => {
		return {
			label: item.name,
			value: item.id,
		}
	})
})

const expensesOptions = computed(() => {
	if (!expensesData.value) return []

	return expensesData.value.map((item) => {
		return {
			label: item.name,
			value: item.id,
		}
	})
})

watch(() => state.category, (newValue, oldValue) => {
	if (newValue === oldValue || !newValue) return

	state.expense = null
	expensesRequest({
		categoryId: newValue,
	})
})

watchEffect(() => {
	if (categoriesError.value || expensesError.value) {
		toast({
			title: 'Erro ao buscar dados.',
			description: 'Tente novamente mais tarde.',
			variant: 'error',
		})
	}
})

onMounted(() => {
	categoriesRequest();
});

function handleCancelClick() {
	state.amount = null;
	state.category = null;
	state.expense = null;
	state.description = '';
	emits('close');
}

async function handleSubmit() {
	try {
		await postTransactionRequest({
			amount: state.amount,
			description: state.description,
			expenseId: state.expense,
		})

		emits('completed')
		emits('close')
	} catch {
		toast.add({
			title: 'Erro ao salvar transação.',
			description: 'Tente novamente mais tarde.',
			variant: 'error',
		})
	}
}

</script>
