<template>
	<UApp :toaster="{ position: 'top-right' }">
		<RouterView />

		<UNavigationMenu
			:items="menuItems"
			:ui="uiConfig"
		/>
	</UApp>
</template>

<script setup>

const menuItems = [
	{
		label: 'Home',
		icon: 'i-lucide-layout-dashboard',
		to: '/'
	},
	{
		label: 'Categorias',
		icon: 'i-lucide-wallet-cards',
		to: '/categories'
	},
	{
		label: 'Gastos',
		icon: 'i-lucide-banknote-arrow-up',
		to: '/expenses'
	}
]

const uiConfig = {
	root: 'flex gap-1.5 [&>div]:min-w-0 [&>div]:w-full',  
	item: 'w-full',
	link: 'h-16 px-2 flex justify-center',
}

</script>