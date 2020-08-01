<template>
  <b-container class="bv-example-row">
  	<table class="table table-hover">
    <thead>
      <tr>
        <th>Instrument</th>
        <th>Price</th>
        <th>Quantity</th>
        <th>Pending Qty</th>
        <th>Order Type</th>
        <th>Status</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="order in orders" :key="order.id">
        <td>{{ order.share }}</td>
        <td>{{ order.price }}</td>
        <td>{{ order.quantity }}</td>
        <td>{{ order.updated_quantity }}</td>
        <td><b-badge :variant="getOrderType(order)">{{ order.order_type }}</b-badge></td>
        <td><b-badge>{{ order.order_status }}</b-badge></td>
        <td><b-button variant="danger" size="sm" :disabled="order.updated_quantity==0" @click="cancelOrder()">Cancel Order</b-button></td>

      </tr>
    </tbody>
  </table>                  
  </tr>
</b-container>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import { authHeader } from '../_helpers/auth-header'
export default {
  props: [
    "orders"
  ],
  methods: {
    getOrderType(order) {
      if(order.order_type == "BUY") {
        return "success";
      }
      else {
        return "danger"
      }
    },
    cancelOrder() {
      const axios_request = {
        url: 'http://127.0.0.1:8000/apiv0/order/cancel/',
        method: 'POST',
        headers: authHeader(),
      };
      axios(axios_request)
      .then(response => (this.info = response.data))
    }
  }
}
</script>