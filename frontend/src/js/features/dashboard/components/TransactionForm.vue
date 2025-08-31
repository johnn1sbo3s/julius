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
				name="transactionValue"
				required
			>
				<UInput
					v-model="state.transactionValue"
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
					:items="Object.values(Category)"
				/>
			</UFormField>

			<UFormField
				label="Descrição"
				name="transactionDescription"
			>
				<UInput
					v-model="state.transactionDescription"
					class="w-full"
					size="xl"
					type="text"
				/>
			</UFormField>

			<div class="flex gap-2">
				<UButton
					class="w-full justify-center cursor-pointer"
					size="xl"
					icon="i-lucide-ban"
					color="neutral"
					@click="handleCancelClick"
				>
					Cancelar
				</UButton>

				<UButton
					class="w-full justify-center cursor-pointer"
					size="xl"
					icon="i-lucide-check"
					type="submit"
				>
					Confirmar
				</UButton>
			</div>
		</UForm>
	</div>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'
import * as v from 'valibot'
import type { FormSubmitEvent } from '@nuxt/ui'

const emits = defineEmits(['close']);

enum Category {
	Food = 'Alimentação',
	Transport = 'Transporte',
	Entertainment = 'Compras e Entretenimento',
	Fixed = 'Gastos Fixos',
}

const state = reactive({
	transactionValue: null,
	transactionDescription: '',
	category: null,
});

const schema = v.object({
	transactionValue: v.pipe(
		v.number('O valor deve ser um número.'),
		v.minValue(1, 'O valor deve ser maior que zero.'),
	),
	transactionDescription: v.string('Por favor, insira uma descrição válida.'),
	category: v.enum(Category, 'Por favor, escolha uma categoria válida.'),
});

type Schema = v.InferOutput<typeof schema>

function handleCancelClick() {
	state.transactionValue = null;
	state.category = null;
	emits('close');
}

function handleSubmit(event: FormSubmitEvent<Schema>) {
	console.log(event.data);
	emits('close');
}

</script>
