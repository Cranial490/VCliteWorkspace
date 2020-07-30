<template>
  <b-container class="bidorders">
    <table class="table table-hover">
    <thead>
      <tr>
        <th>Buy Price</th>
        <th>Quantity</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="bid in bids" :key="bid.id" @click="fetchBidPrice(bid.bid_price)">
        <td>{{ bid.bid_price }}</td>
        <td>{{ bid.quantity }}</td>
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
    "bids"
  ],
  methods: {
  fetchBidPrice(price) {
     this.$store.commit("updateCurrSellPrice", price);
     bus.$emit('updateTabIndex', 1);
    }
  }
}
</script>