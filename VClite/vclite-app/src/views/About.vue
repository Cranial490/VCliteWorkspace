<template>
  <div class="content">
    <h1>About</h1>
    <p>{{  }}</p>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import { authHeader } from '../_helpers/auth-header'

export default {
  components: {
  },
  data () {
  	return {
      info: [],
  	}
  },
  methods: {
    orderExec() {
      const axios_request = {
        url: 'http://127.0.0.1:8000/apiv0/order/execute/',
        method: 'POST',
        headers: authHeader(),
        data: {
          price:'1', 
          quantity:'12', 
          totalAmount:'21', 
          brokerage:'', 
          user: '1', 
          share:'1'
        }
    };
      axios(axios_request)
      .then(response => (this.info = response.data))
    }
  },
  created() {
    this.orderExec()
  },
}
</script>