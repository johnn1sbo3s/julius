<template>
	<div class="flex flex-col gap-3 items-center justify-center flex-1">
		<section class="text-center">
			<h1 class="font-semibold">
				Seja bem vindo!
			</h1>

			<p>Entre com suas credenciais para continuar</p>

			<UForm
				class="mt-8 flex flex-col gap-3"
				:state="state"
				:schema="schema"
				@submit="handleSubmit"
			>
				<UFormField
					label="E-mail"
					name="email"
					required
				>
					<UInput
						v-model="state.email"
						class="w-full"
						size="xl"
						type="email"
					/>
				</UFormField>

				<UFormField
					label="Senha"
					name="password"
					required
				>
					<UInput
						v-model="state.password"
						class="w-full"
						size="xl"
						type="password"
					/>
				</UFormField>

				<UButton
					class="w-full justify-center mt-2"
					size="xl"
					type="submit"
				>
					Entrar
				</UButton>
			</UForm>

			<div class="flex flex-col gap-2 my-4 w-full">
				<USeparator>ou</USeparator>

				<div class="flex gap-1 justify-center w-full">
					<span>Não possui conta?</span>

					<ULink
						to="/register"
						class="text-primary-500 hover:text-primary-600"
					>
						Cadastre-se
					</ULink>
				</div>
			</div>
		</section>
	</div>
</template>

<script lang="ts" setup>
import { reactive } from 'vue'
import * as v from 'valibot'
import type { FormSubmitEvent } from '@nuxt/ui'

const state = reactive({
	email: '',
	password: '',
});

const schema = v.object({
	email: v.pipe(
		v.string('Insira um e-mail válido.'),
		v.email('O e-mail não é válido.'),
		v.maxLength(30, 'O e-mail deve ter no máximo 30 caracteres.'),
	),
	password: v.pipe(
		v.string('Insira uma senha válida.'),
		v.minLength(8, 'A senha deve ter no mínimo 8 caracteres.'),
	),
});

type Schema = v.InferOutput<typeof schema>

function handleSubmit(event: FormSubmitEvent<Schema>) {
	console.log(event.data);
}

</script>