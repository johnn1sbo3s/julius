export function formatCurrency(value) {
	if (value == null) return null

	return new Intl.NumberFormat('pt-BR', {
		style: 'currency',
		currency: 'BRL',
	}).format(value)
}