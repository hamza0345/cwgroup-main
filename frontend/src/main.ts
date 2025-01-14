import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import { createPinia } from 'pinia'

const app = createApp(App)

app.use(router)
app.use(createPinia())
app.mount('#app')
