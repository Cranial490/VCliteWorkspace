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
  	postOrder(price, qty, user, share, order_type) {
      const axios_request = {
        url: 'http://127.0.0.1:8000/apiv0/order/execute/',
        method: 'POST',
        headers: authHeader(),
        data: {
          price: price,
          quantity: qty,
          updated_quantity: qty,
          user: user, 
          share: share,
          order_type: order_type
        }
    };
      axios(axios_request)
      .then(response => (this.info = response.data))
    }
  },
  created() {
  	this.postOrder('15', '4', 'pranjal', 'BBQ', 'BUY')
  },
}
</script>