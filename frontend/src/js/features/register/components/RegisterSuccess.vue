<template>
	<div class="w-full grow-1 flex flex-col justify-center items-center gap-5 relative">
		<div class="pointer-events-none fixed inset-0 overflow-hidden">
			<div class="h-[300px] w-[300px] absolute -top-20 -left-20 bg-yellow-300/5 rounded-full blur-3xl" />

			<div class="h-[300px] w-[300px] absolute bottom-20 -right-20 bg-yellow-600/4 rounded-full blur-3xl" />
		</div>

		<img
			src="/img/success.svg"
			alt="Ícone de sucesso"
			width="80"
			height="80"
		>

		<div class="flex flex-col gap-2 text-center max-w-[80%]">
			<h1 class="text-white font-semibold">
				Cadastro realizado!
			</h1>

			<p>Parabéns!!🎉🥳 Você deu o primeiro passo rumo ao controle de suas finanças.</p>
		</div>

		<UButton
			class="w-full justify-center mt-5 cursor-pointer z-10"
			size="xl"
			@click="handleLoginClick"
		>
			Ir para o login
		</UButton>
	</div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function handleLoginClick() {
	router.push({ name: 'login' })
}

</script>

<style lang="scss" scoped>

</style>