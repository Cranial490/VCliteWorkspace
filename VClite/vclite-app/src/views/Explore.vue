<template>
  <div class="content">
    <h1>Explore</h1>
    <Carousel></Carousel>
  </div>
</template>


<script>
// @ is an alias to /src
import Carousel from '@/components/Carousel.vue'
export default {
  components: {
  	Carousel
  }
}
</script>

<style>
.content {
  width:75%;
    float:right;
}
</style>
