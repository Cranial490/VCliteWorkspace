<template>
  <div id="app">
    <div id="nav" v-if="isNavVisible">
      <top-header></top-header>
    </div>
    <div id="sidebar">
      <side-bar></side-bar>
    </div>
    <router-view/>
  </div>
</template>

<script>
// @ is an alias to /src
import NavBar from '@/components/NavBar.vue'
import SideBar from '@/components/SideBar.vue'
export default {
  components: {
    "top-header": NavBar,
    "side-bar": SideBar
  },
  computed: {
    isNavVisible: function() {
      if(this.$route.name === "Login" || this.$route.name === "Register1" || this.$route.name === "Register2" || this.$route.name === "Register3" || this.$route.name === "Forgot" || this.$route.name === "Forgot2" || this.$route.name === "changePassword" || this.$route.name === "changePassword2") {
        return false;
      }
      else {
        return true;
      }
    }
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
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
