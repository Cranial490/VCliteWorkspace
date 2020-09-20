<template>
	<div class="sidenav" v-if="isSideVisible">
    <div class="orders">
      <OrderWindow v-if="$route.params.shareid"></OrderWindow>
      <hr>
    </div>
    <!-- <input class="search" type="text"><hr> -->
</div>
</template>



<script>
import OrderWindow from '@/components/OrderWindow.vue'
export default {
  components: {
    OrderWindow,
  },
  computed: {
    isSideVisible: function() {
      if(this.$route.name === "Login"  || this.$route.name === "Register1" || this.$route.name === "Register2" || this.$route.name === "Register3" || this.$route.name === "Forgot" || this.$route.name === "Forgot2" || this.$route.name === "changePassword" || this.$route.name === "changePassword2") {
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
  body {
    font-family: "Avenir", "Helvetica", "Arial", sans-serif;
  }

  .sidenav {
    height: 100%;
    width: 25%;
    position: fixed;
    z-index: 1;
    left: 0;
    background-color: #f8f9fa;
    overflow-x: hidden;
    padding-top: 20px;
  }

  .sidenav a {
    padding: 6px 8px 6px 16px;
    text-decoration: none;
    font-size: 25px;
    color: #818181;
    display: block;
  }

  .sidenav a:hover {
    color: #f1f1f1;
  }

  .search {
    width: 90%;
    border: none;
    line-height: 3em;
    outline-width: 0;
    background-color: #f8f9fa;
  }
  .main {
    margin-left: 160px; /* Same as the width of the sidenav */
    font-size: 28px; /* Increased text to enable scrolling */
    padding: 0px 10px;
  }

  @media screen and (max-height: 450px) {
    .sidenav {padding-top: 15px;}
    .sidenav a {font-size: 18px;}
  }
</style>