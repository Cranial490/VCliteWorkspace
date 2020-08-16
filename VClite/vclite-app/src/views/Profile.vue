<template>
	<div class="content">
    <h1>Profile</h1>
   	<div class="user-info">
   		<b-card title="" body-class="text-center" header-tag="nav">
	    <template v-slot:header>
	      <b-nav card-header tabs>
	        <!-- <b-nav-item active></b-nav-item> -->
	        <b-link class="edit" to="/edit"><b>EDIT</b></b-link>
	      </b-nav>
	    </template>

	    <b-card-text>
	      <p class= "user-field" id="username"><b>Username:</b> {{ userData[0].username }}</p><br>		   
		  <p class= "user-field" id="name"><b>Name:</b> {{ userData[0].first_name }} {{ userData[0].last_name }}</p><br>
	      <p class= "user-field" id="email"><b>Email:</b> {{ userData[0].email }}</p><br>
	      <p class= "user-field" id="phone"><b>Phone:</b> {{ userData[0].phone_no}}</p><br>
	      <p class= "user-field" id="dpid"><b>DPID:</b> {{ userData[0].dpid}}</p><br>
	      <p class= "user-field" id="pan"><b>PAN:</b> {{ userData[0].pan_no}}</p><br>
	    </b-card-text>

	  </b-card>
   	</div>
  </div>
</template>
<script>
// @ is an alias to /src

export default {
 data () {
 	return {
 		userData: this.$store.state.userLog,
 	}
 },
  components: {
  }
}
</script>

<style>
.content {
  width:75%;
  float:right;
}
.user-field{
	float:left;
	margin-left:30%;
	margin-bottom:10px;
}
p {
    margin-top: 0;
    margin-bottom: 0;
}
.edit {
	float:right;
	margin-bottom:10px;
}
.user-info {
	width: 500px;
	margin-left:30%;
}
</style>