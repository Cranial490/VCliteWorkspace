<template>
  <div class="content">
    <h1>Position</h1>
    <OrderTable :orders="getOpenOrders" :isVisible="true"></OrderTable>
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
  		orders: [],
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
  	// this.$store.dispatch('getOrders');
    this.getOrders();
  },  
  computed: {
  	 getOpenOrders() {
      return this.orders.filter((order)=>{
        if(order.order_status == "EXECUTED" || order.order_status == "SUBMITTED") {
          return order
        }
      })
    }
  }
}
</script>

<style>
.content {
	width:75%;
    float:right;
}
</style>
