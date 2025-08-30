<template>
	<div class="flex flex-col gap-3 items-center justify-center flex-1">
		<section class="text-center">
			<h1 class="font-semibold">
				Seja bem-vindo(a)!
			</h1>

			<p>Entre com suas credenciais para continuar</p>

			<UForm
				ref="form"
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
						:type="showPassword ? 'text' : 'password'"
					>
						<template #trailing>
							<UButton
								color="neutral"
								variant="link"
								size="sm"
								aria-controls="password"
								:icon="showPassword ? 'i-lucide-eye-off' : 'i-lucide-eye'"
								:aria-label="showPassword ? 'Esconder senha' : 'Mostrar senha'"
								:aria-pressed="showPassword"
								@click="showPassword = !showPassword"
							/>
						</template>
					</UInput>
				</UFormField>

				<UButton
					class="w-full justify-center mt-2"
					size="xl"
					type="submit"
					:loading="loading"
				>
					Entrar
				</UButton>
			</UForm>

			<div class="flex flex-col gap-2 my-4 w-full">
				<USeparator>ou</USeparator>

				<div class="flex gap-1 justify-center w-full">
					<span>Não possui conta?</span>

					<ULink
						class="text-primary-500 hover:text-primary-600"
						:to="{ name: 'register' }"
					>
						Cadastre-se
					</ULink>
				</div>
			</div>
		</section>
	</div>
</template>

<script setup>
import { ref, reactive, useTemplateRef } from 'vue'
import { login } from '@/js/core/services/auth'
import { useApi } from '@/js/shared/composables/useApi'
import { useRouter } from 'vue-router'
import * as v from 'valibot'

const toast = useToast()
const router = useRouter()
const { request: loginRequest, error, loading } = useApi(login);

const showPassword = ref(false);
const form = useTemplateRef('form')

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

async function handleSubmit(event) {
	try {
		const response = await loginRequest(event.data)
		if (response.access_token) {
			localStorage.setItem('token', response.access_token)
			router.push('/')
		}
	} catch (e) {
		state.email = ''
		state.password = ''
		form.value.clear()
		toast.add({
			title: error.value.detail,
			color: 'error',
		})
	}
}

</script>