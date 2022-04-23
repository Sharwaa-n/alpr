import axios from 'axios'

export default {
    install(Vue) {
        // 1. add global method or property
        Vue.prototype.$api = axios;
      
    }
}