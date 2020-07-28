<template>
  <div class="content">
    <h1>About</h1>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import { authHeader } from '../_helpers/auth-header'
export default {
  components: {
  },
  methods: {
  	postOrder() {
      const axios_request = {
        url: 'http://127.0.0.1:8000/apiv0/order/execute/',
        method: 'POST',
        headers: authHeader(),
        data: {
          price:'20',
          quantity:'3', 
          updated_quantity:'3',
          user: 'cranial', 
          share:'BBQ',
          order_type:'SELL'
        }
    };
      axios(axios_request)
      .then(response => (this.info = response.data))
    }
  },
  created() {
  	this.postOrder()
  },
}
</script>