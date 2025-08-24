<template>
	<div class="text-red-400">
		<UButton @click="openTransactionModal">Nova Transação</UButton>
	</div>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router';

const router = useRouter();

function openTransactionModal() {
	router.push('/transaction/new');
}

</script>

<style lang="scss" scoped></style>
