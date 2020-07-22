<template>
  <div class="content">
    <h1>Terminal</h1>
  	<b-container class="bv-example-row">
	  <b-row>
	    <b-col>BUY ORDERS<BidTable :bids="bids"></BidTable></b-col>
	    <b-col>SELL ORDERS<AskTable :asks="asks"></AskTable></b-col>
	  </b-row>
	</b-container>
	<hr>
	
  </div>
</template>

<script>
import axios from 'axios';
import AskTable from '@/components/AskTable.vue'
import BidTable from '@/components/BidTable.vue'
import OrderWindow from '@/components/OrderWindow.vue'
import { authHeader } from '../_helpers/auth-header'

export default {
  data() {
  	return {
  		asks: [],
  		bids: [],
  		share_id: this.$route.params.shareid
  	}
  },
  components: {
  	AskTable,
  	BidTable,
  	OrderWindow
  },
  methods: {
  	getAsks(){
  	axios.get("http://127.0.0.1:8000/apiv0/asks/", {params: {share_id: this.share_id}, headers: authHeader() })
      .then(res => (this.asks = res.data))
      .catch(err => console.log(err));
  	},
  	getBids(){
  	axios.get("http://127.0.0.1:8000/apiv0/bids/", {params: {share_id: this.share_id}, headers: authHeader() })
      .then(res => (this.bids = res.data))  
      .catch(err => console.log(err));
  	}
  },
  created() {
  	this.getBids();
  	this.getAsks();
  }
}
</script>
<style>
.content {
  width:75%;
    float:right;
}
</style>