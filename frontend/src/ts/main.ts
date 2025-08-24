import '@/css/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import ui from '@nuxt/ui/vue-plugin'

import App from '@/ts/App.vue'
import router from '@/ts/core/routes/index'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ui)

app.mount('#app')
