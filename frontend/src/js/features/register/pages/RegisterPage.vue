<template>
	<div class="flex flex-col gap-3 items-center justify-center flex-1 overflow-clip">
		<section
			v-if="!showRegisterSuccess"
			class="text-center"
		>
			<h1 class="font-semibold">
				Cadastre-se
			</h1>

			<p>Preencha os dados abaixo para criar sua conta</p>

			<UForm
				ref="form"
				class="mt-8 flex flex-col gap-3"
				:state="state"
				:schema="schema"
				@submit="handleSubmit"
			>
				<UFormField
					label="Nome"
					name="name"
					required
				>
					<UInput
						v-model="state.name"
						class="w-full"
						size="xl"
						type="text"
					/>
				</UFormField>

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

				<UFormField
					label="Confirmar senha"
					name="confirmPassword"
					required
				>
					<UInput
						v-model="state.confirmPassword"
						class="w-full"
						size="xl"
						:type="showConfirmPassword ? 'text' : 'password'"
					>
						<template #trailing>
							<UButton
								color="neutral"
								variant="link"
								size="sm"
								aria-controls="password"
								:icon="showConfirmPassword ? 'i-lucide-eye-off' : 'i-lucide-eye'"
								:aria-label="showConfirmPassword ? 'Esconder senha' : 'Mostrar senha'"
								:aria-pressed="showConfirmPassword"
								@click="showConfirmPassword = !showConfirmPassword"
							/>
						</template>
					</UInput>
				</UFormField>

				<UButton
					class="w-full justify-center mt-2 cursor-pointer"
					size="xl"
					type="submit"
					:loading="loading"
				>
					Cadastrar
				</UButton>
			</UForm>

			<div class="flex flex-col gap-2 my-4 w-full">
				<USeparator>ou</USeparator>

				<div class="flex gap-1 justify-center w-full">
					<span>Já tem uma conta?</span>

					<ULink
						class="text-primary-500 hover:text-primary-600"
						:to="{ name: 'login-page' }"
					>
						Entre
					</ULink>
				</div>
			</div>
		</section>

		<RegisterSuccess v-else />
	</div>
</template>

<script setup>
import { ref, reactive, useTemplateRef } from 'vue'
import { register } from '@/js/core/services/auth'
import { useApi } from '@/js/shared/composables/useApi'
import RegisterSuccess from '@/js/features/register/components/RegisterSuccess.vue'
import * as v from 'valibot'

const toast = useToast()
const { request: registerRequest, error, loading } = useApi(register);

const showPassword = ref(false)
const showConfirmPassword = ref(false)
const showRegisterSuccess = ref(false)

const form = useTemplateRef('form')

const state = reactive({
	name: '',
	email: '',
	password: '',
	confirmPassword: '',
});

const schema = v.pipe(
	v.object({
		name: v.pipe(
			v.string('Insira um nome válido.'),
			v.minLength(3, 'O nome deve ter no mínimo 3 caracteres.'),
			v.maxLength(30, 'O nome deve ter no máximo 30 caracteres.'),
		),
		email: v.pipe(
			v.string('Insira um e-mail válido.'),
			v.email('O e-mail não é válido.'),
			v.maxLength(30, 'O e-mail deve ter no máximo 30 caracteres.'),
		),
		password: v.pipe(
			v.string('Insira uma senha válida.'),
			v.minLength(8, 'A senha deve ter no mínimo 8 caracteres.'),
		),
		confirmPassword: v.string('Insira uma senha válida.'),
	}),
	v.forward(
		v.partialCheck(
			[['password'], ['confirmPassword']],
			(input) => input.password === input.confirmPassword,
			'As senhas não coincidem.',
		),
		['confirmPassword'],
	),
)

async function handleSubmit(event) {
	try {
		await registerRequest(event.data)
		showRegisterSuccess.value = true
	} catch {
		state.name = '',
		state.email = '',
		state.password = '',
		state.confirmPassword = '',
		form.value.clear()
		toast.add({
			title: error.value.detail,
			color: 'error',
		})
	}
}
</script>

<style lang="scss" scoped>

</style>