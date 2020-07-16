<template>
  
</template>

<script>
// @ is an alias to /src
import axios from 'axios';

export default {
  name: 'Home',
  data() {
  	return {
  		shares: []
  	}
  },
  components: {
  },
  methods: {
  	getShares(){
  	axios.get("http://127.0.0.1:8000/apiv0/shares/")
      .then(res => (this.shares = res.data))  
      .catch(err => console.log(err));
  	}
  },
  created() {
  	this.getShares()
  }
}
</script>