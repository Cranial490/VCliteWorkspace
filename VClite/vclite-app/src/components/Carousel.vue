<template>
  <b-container>
    <carousel-3d :controls-visible="true" :controls-prev-html="'&#10092;'" :controls-next-html="'&#10093;'" 
               :controls-width="30" :controls-height="60" :clickable="false">
    <slide v-for="(slide, i) in $store.state.shares" :index="i" :key="i" :style= "{
           'height': '260px',
           'border-radius': '20px',
           'border-color': '#ffff',
           'background-color': '#cccccc03'
         }">
      <figure>
        <b-card-group deck>
          <b-card
            header="Featured"
            header-tag="header"
            >
            <b-card-title>{{ slide.name }}</b-card-title>
            <b-card-text>{{ slide.description }}</b-card-text>
            <b-button @click="getDetails()" variant="primary">Details</b-button>
            <template v-slot:footer>
              <small class="text" :style="{'font-size': 'larger', 'font-weight':'bold'}">LTP: Rs.{{ slide.ltp }}</small>
            </template>
          </b-card>
        </b-card-group>
      </figure>
    </slide>
  </carousel-3d>
</b-container>
</template>

<script>
// @ is an alias to /src
import { Carousel3d, Slide } from 'vue-carousel-3d';
export default {
  components: {
    Carousel3d,
    Slide
  },
  methods: {
    getDetails() {
      alert("hello");
    }
  }
}
</script>
