<template>
  <div class="content">
    <h1>Orders</h1>
    <OrderTable :orders="orders"></OrderTable>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import { authHeader } from '../_helpers/auth-header'
import OrderTable from '@/components/OrderTable.vue'

export default {
  components: {
  	OrderTable,
  },
  data() {
  	return {
  		orders: []
  	}
  },
  methods: {
  	getOrders() {
  	axios.get("http://127.0.0.1:8000/apiv0/order/", {headers: authHeader()})
      .then(res => (this.orders = res.data))
      .catch(err => console.log(err));
  	}
  },
  created() {
  	this.getOrders()
  }

}
</script>

<style>
.content {
	width:75%;
    float:right;
}
</style>