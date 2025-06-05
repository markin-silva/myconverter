import { createApp } from 'vue'
import App from './App.vue'
import keycloak from './keycloak'

keycloak.init({ onLoad: 'login-required' }).then(authenticated => {
  if (authenticated) {
    const app = createApp(App)
    app.config.globalProperties.$keycloak = keycloak
    app.mount('#app')
  } else {
    window.location.reload()
  }
}).catch(() => {
  console.log('Failed to initialize Keycloak')
})
