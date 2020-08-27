<template>
  <b-container class="askorders">
    <table class="table table-hover">
    <thead>
      <tr>
        <th>Sell Price</th>
        <th>Quantity</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="ask in asks" :key="ask.id" @click="fetchAskPrice(ask.ask_price)">
        <td>{{ ask.ask_price }}</td>
        <td>{{ ask.quantity }}</td>
      </tr>
    </tbody>
  </table>                  
  </tr>
</b-container>
</template>

<script>
// @ is an alias to /src
import { bus } from '../main'
export default {
  props: [
    "asks"
  ],
  methods: {
  fetchAskPrice(price) {
     this.$store.commit("updateCurrBuyPrice", price);
     bus.$emit('updateTabIndex', 0);
    }
  }
}
</script>