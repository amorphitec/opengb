import VueRouter from 'vue-router'
import Vue from 'vue'
Vue.use(VueRouter)
Vue.config.debug = true

// application
import App from './App.vue'

// libs and services
require('./css/foundation.css')
require('./css/foundation-icons/foundation-icons.css')

// pages
import HomePage from './pages/Home.vue'
import SettingsPage from './pages/Settings.vue'

/* eslint-disable no-new */
// new Vue({
//   el: 'body',
//   components: { App }
// })

var router = new VueRouter()

// Define some routes.
// Each route should map to a component. The 'component' can
// either be an actual component constructor created via
// Vue.extend(), or just a component options object.
// We'll talk about nested routes later.
router.map(
	{
		'/home': {
			component: HomePage
		},
		'/settings': {
			component: SettingsPage
		}
	}
)

// Now we can start the app!
// The router will create an instance of App and mount to
// the element matching the selector #app.
router.start(App, '#main-body')
