<template>
	<div class="content">
    <h1>Profile</h1>
   	<div class="header">User Details
	</div>
	<div class="edit-link"> <b-link to="/edit">Edit</b-link>
	</div><br>
   	<hr>
   	<div class="user-profile">
    <div class="userDeets-1">
    	<b-container class="bv-example-row">
		  <b-row>
		    <b-col>Name: {{ userData[0].username }}</b-col>
		    <b-col>Email: pranjal.paliwal@gmail.com</b-col>
		    <b-col></b-col>
		  </b-row>
		</b-container>
    </div>
    <div class="userDeets-2">
    	<b-container class="bv-example-row">
		  <b-row>
		    <b-col><label>First Name:</label> <span>Pranjal</span></b-col>
		    <b-col><label>Last Name:</label> Paliwal</b-col>
		    <b-col></b-col>
		  </b-row>
		</b-container>
    </div>
 	<div class="userDeets-3">
    	<b-container class="bv-example-row">
		  <b-row>
		    <b-col><label>Phone No:</label> <span>9783581492</span></b-col>
		    <b-col><label>DPID:</label> 12345678</b-col>
		    <b-col></b-col>
		  </b-row>
		</b-container>
    </div>
	</div>
    <hr>
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
.userDeets-1 {
  /*border: 1px solid;*/
  margin: 20px;
  height: 40px;

}
.userDeets-2 {
  /*border: 1px solid;*/
  margin: 0px;
  height: 25px;

}
.userDeets-3 {
  /*border: 1px solid;*/
  margin: 20px;
  height: 25px;

}
.user-profile {
	height: 120px;
}
.header {
	float: left;
	margin-left: 20px;
	margin-bottom: 0px;
	font-size:30px;

}
.edit-link {
	float: right;
}
</style>