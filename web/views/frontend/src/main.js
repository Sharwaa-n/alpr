import Vue from 'vue'
import App from './App.vue'

import Home from './views/Home'
import Detect from './views/Detect'
import Etc from './views/Etc'
import Lost from './views/Lost'


import VueRouter from 'vue-router'

import axios from './plugins/axios'

Vue.use(VueRouter)
Vue.use(axios)

const routes = [
  { path: '/', component: Home },
  { path: '/detect', component: Detect },
  { path: '/lost', component: Lost },
  { path: '/support', component: Etc  }
]

const router = new VueRouter({
  routes // short for `routes: routes`
})


Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
