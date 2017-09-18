<template>
  <div id="app">
    <mu-appbar title="Password Manager">
      <!-- <mu-flat-button color="white" label="flat Button" slot="right" @click="addPassword"></mu-flat-button> -->
    </mu-appbar>
<!--     <img src="./assets/logo.png"> -->
    <Pwmanager
      class="pwmanager"
    />
  </div>
</template>

<script>
import Pwmanager from '~/components/Pwmanager.vue'
import Vue from 'vue'
import MuseUI from 'muse-ui'
import DatabaseBroker from '~/assets/DatabaseBroker.js'
import 'muse-ui/dist/muse-ui.css'
Vue.use(MuseUI)

let header = {
  'X-Parse-Application-Id': 'wggesucht',
  'X-Parse-REST-API-Key': 'wggesucht',
  'Content-Type': 'application/json',
}
export default {
  components: {
    Pwmanager
  },
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  /*text-align: center;*/
  /*color: #2c3e50;*/
  /*margin-top: 60px;*/
}
.container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.title {
  font-family: "Quicksand", "Source Sans Pro", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; /* 1 */
  display: block;
  font-weight: 300;
  font-size: 100px;
  color: #35495e;
  letter-spacing: 1px;
}

.subtitle {
  font-weight: 300;
  font-size: 42px;
  color: #526488;
  word-spacing: 5px;
  padding-bottom: 15px;
}

.links {
  padding-top: 15px;
}
.pwmanager {
  height:100%;
}
</style>
