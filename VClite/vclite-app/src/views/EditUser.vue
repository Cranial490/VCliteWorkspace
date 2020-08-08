<template>
	<div class="content">
    	<h1>EDIT</h1>

    	<div class="edit-form">
		  <b-input-group size="mt-3" prepend="Username">
		    <b-form-input v-model="username"></b-form-input>
		  </b-input-group>

		  <!-- Using slots -->
		  <b-input-group class="mt-3" prepend="First Name">
		    <b-form-input v-model="firstName"></b-form-input>
		  </b-input-group>

		  <!-- Using slots -->
		  <b-input-group class="mt-3" prepend="Last Name">
		    <b-form-input v-model="lastName"></b-form-input>
		  </b-input-group>

		  <!-- Using slots -->
		  <b-input-group class="mt-3" prepend="Email">
		    <b-form-input v-model="Email"></b-form-input>
		  </b-input-group>

		  <!-- Using slots -->
		  <b-input-group class="mt-3" prepend="Phone No.">
		    <b-form-input v-model="phnNo"></b-form-input>
		  </b-input-group>

		  <b-input-group class="mt-3" prepend="DPID">
		    <b-form-input v-model="dpid"></b-form-input>
		  </b-input-group>

		  <b-button class="mt-3" variant="outline-primary" @click="UpdateData">Button</b-button>
		</div>

	</div>

</template>

// @ is an alias to /src
<script>
  	import axios from 'axios'
	import { authHeader } from '../_helpers/auth-header'
	export default {
	data() {
	  return {
	    username: this.$store.state.userLog[0].username,
	    firstName: this.$store.state.userLog[0].first_name,
	    lastName: this.$store.state.userLog[0].last_name,
	    Email: this.$store.state.userLog[0].email,
	    phnNo: this.$store.state.userLog[0].phone_no,
	    dpid: this.$store.state.userLog[0].dpid,
	  }
	},
	methods: {
	  UpdateData() {
	  	console.log("update initiated")
	  	const axios_request = {
	    url: 'http://127.0.0.1:8000/apiv0/user/update/',
	    method: 'POST',
	    headers: authHeader(),
	    data: {
	    }
	  };
	    axios(axios_request)
	    .then(response => (this.info = response.data))
	    .catch(err => console.log(err));
	  }
	}
	}
</script>

<style>
.content {
  width:75%;
  float:right;
}
.edit-form {
	width:25%;
	margin:10px;
	position: fixed;
    left: 63%;
    transform: translate(-50%, 0);
}
</style>
