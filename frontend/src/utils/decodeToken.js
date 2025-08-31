export function decodeJWT(token) {
	const payload = token.split('.')[1]
	const decoded = atob(payload)

	return JSON.parse(decoded)
}