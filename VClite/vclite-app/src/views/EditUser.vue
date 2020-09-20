<template>
	<div class="content">
    	<h1>EDIT</h1>

    	<div class="edit-form">
        <ValidationObserver ref="form" v-slot="{ handleSubmit }" >
        <b-form @submit.prevent="handleSubmit(UpdateData)">
            <b-input-group size="mt-3" prepend="Username">
                <b-form-input v-model="username" readonly></b-form-input>
            </b-input-group>

		  <!-- Using slots -->
            <b-input-group class="mt-3" prepend="First Name">
                <b-form-input v-model="firstName" readonly></b-form-input>
            </b-input-group>

		  <!-- Using slots -->
            <b-input-group class="mt-3" prepend="Last Name">
                <b-form-input v-model="lastName" readonly></b-form-input>
            </b-input-group>

		  <!-- Using slots -->
          <ValidationProvider rules="required|email" v-slot="{ errors, failedRules, valid }">
            <b-input-group class="mt-3" prepend="Email">
                <b-form-input v-model="Email" :state="errors[0] ? false : (valid ? true : null)"></b-form-input>
                <b-form-invalid-feedback id="inputLiveFeedback">{{ errors[0] }}</b-form-invalid-feedback>
            </b-input-group>
          </ValidationProvider>

		  <!-- Using slots -->
          <ValidationProvider rules="required|min:10|max:10" v-slot="{ errors, failedRules, valid }">
            <b-input-group class="mt-3" prepend="Phone No.">
                <b-form-input v-model="phnNo" :state="errors[0] ? false : (valid ? true : null)"></b-form-input>
                <b-form-invalid-feedback id="inputLiveFeedback">{{ errors[0] }}</b-form-invalid-feedback>
            </b-input-group>
          </ValidationProvider>

          <ValidationProvider rules="required|min:16|max:16" v-slot="{ errors, failedRules, valid }">
            <b-input-group class="mt-3" prepend="DPID">
                <b-form-input v-model="dpid" :state="errors[0] ? false : (valid ? true : null)"></b-form-input>
                <b-form-invalid-feedback id="inputLiveFeedback">{{ errors[0] }}</b-form-invalid-feedback>
            </b-input-group>
          </ValidationProvider>

          <ValidationProvider rules="required|min:10|max:10" v-slot="{ errors, valid }">
            <b-input-group class="mt-3" prepend="PAN">
                <b-form-input v-model="pan" :state="errors[0] ? false : (valid ? true : null)"></b-form-input>
                <b-form-invalid-feedback id="inputLiveFeedback2">{{ errors[0] }}</b-form-invalid-feedback>
            </b-input-group>
          </ValidationProvider>

		    <b-button class="mt-3" variant="outline-primary" type="submit">Save</b-button>
        </b-form>
        </ValidationObserver>
		</div>

	</div>

</template>

// @ is an alias to /src
<script>
  	import axios from 'axios'
    import { authHeader } from '../_helpers/auth-header'
    import { mapState, mapActions } from 'vuex'
	export default {
	data() {
	  return {
	    username: this.$store.state.userLog[0].username,
	    firstName: this.$store.state.userLog[0].first_name,
	    lastName: this.$store.state.userLog[0].last_name,
	    Email: this.$store.state.userLog[0].email,
	    phnNo: this.$store.state.userLog[0].phone_no,
	    dpid: this.$store.state.userLog[0].dpid,
	    pan: this.$store.state.userLog[0].pan_no
	  }
	},
	methods: {
      ...mapActions('account', ['handleFault']),
	  UpdateData() {
        console.log("update initiated")
        console.log("email = ", this.Email)
	  	const axios_request = {
	    url: 'http://127.0.0.1:8000/apiv0/user/update/',
	    method: 'POST',
	    headers: authHeader(),
	    data: {
	    	id: this.$store.state.userLog[0].id,
	    	username: this.username,
	    	email:this.Email,
	    	phone_no:this.phnNo,
	    	dpid:this.dpid,
	    	pan_no:this.pan
	    }
	  };
	    axios(axios_request)
	    .then(response => (this.info = response.data))
	    .then(alert("Saved"))
	    .then(this.$router.push('Home'))
	    .then(this.$router.go())
	    .catch(err => this.handleFault(err));
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
.form-control[readonly] {
    background-color: #f6f5fb	;
    opacity: 1;
}
</style>