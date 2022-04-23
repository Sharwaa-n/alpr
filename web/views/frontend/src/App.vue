<template>
  <div>
    <v-nav></v-nav>
    <div class="container pt-4">
      <router-view></router-view>
    </div>
    <v-footer></v-footer>
  </div>
</template>

<script>

import Footer from './components/Footer'
import Nav from './components/Nav'

export default {
  name: 'App',
  components: {
    'v-footer':  Footer, 
    'v-nav': Nav
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
