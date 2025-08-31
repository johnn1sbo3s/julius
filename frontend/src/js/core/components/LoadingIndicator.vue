<template>
	<div class="loading-indicator" />
</template>

<script setup>
import { computed, ref, watch } from 'vue';

// Props
const props = defineProps({
	/**
	 * Controla a exibição do LoadingIndicator.
	 */
	modelValue: {
		type: Boolean,
		required: true,
	},
	/**
	 * A cor em hexadecimal.
	 */
	color: {
		type: String,
		default: '#fdc700',
	},
	/**
	 * Define o tempo, em ms, do intervalo de mudança da barra de progresso.
	 */
	intervalTime: {
		type: Number,
		default: 500,
	},
	/**
	 * Define se o tipo de dispositivo é mobile.
	 */
	mobile: {
		type: Boolean,
		default: false,
	},
});

// Variáveis reativas
const currentPercentage = ref(0);

// Variáveis computadas
const barPercentage = computed(() => {
	return `${currentPercentage.value}%`;
});

const disabledTransition = computed(() => {
	return currentPercentage.value === 0 ? 'none' : 'width 0.5s';
});

const barHeight = computed(() => {
	if (props.mobile) {
		return '4px';
	}

	return '3px';
})

const computedColor = computed(() => props.color);

// Watch
watch(() => props.modelValue, (newValue) => {
	if (newValue) {
		start();
		increment();
		return;
	}

	finish();
});

// Métodos
function start() {
	currentPercentage.value = 1;
}

function increment() {
	if (currentPercentage.value > 0 && currentPercentage.value < 90) {
		currentPercentage.value += Math.floor(Math.random() * (25 - 10 + 1) + 10);

		if (currentPercentage.value >= 90) {
			currentPercentage.value = 90;
			return;
		}

		let randomInterval = Math.floor(Math.random() * ((props.intervalTime * 1.4) - (props.intervalTime * 0.5)) + (props.intervalTime * 0.5));
		setTimeout(increment, randomInterval);
	}
}

function finish() {
	currentPercentage.value = 100;
	setTimeout(() => {
		currentPercentage.value = 0;
	}, 600);
}

</script>

<style lang="scss" scoped>

.loading-indicator {
	position: fixed;
	top: 0;
	left: 0;
	width: v-bind(barPercentage);
	height: 4px;
	display: flex;
	justify-content: center;
	align-items: center;
	background-color: v-bind(computedColor);
	background-size: 200% 100%;
	animation: loading-gradient 2s ease infinite;
	z-index: 5000;
	transition: v-bind(disabledTransition);

	@keyframes loading-gradient {
		0% {
			background-position: 0% 0%;
		}
		100% {
			background-position: -100% 0%;
		}
	}
}
</style>