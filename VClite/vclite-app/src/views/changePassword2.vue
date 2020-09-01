<template>
	<b-container class="loginBox">
	<div class="loginContent shadow">
		<h1>
			Your Password updated successfully
		</h1>
		<router-link to="/login" class="btn btn-link">Continue to Login</router-link>
	</div>
	</b-container>
</template>

<style>
.loginContent {
  border:1px solid;
  border-color: #8c8f946b;
  border-radius:10px;
  padding:30px;
  background-color: #ffff;
  margin-top: 100px;
  /*width:50%;*/
}
.loginBox {
    width:35%;
    height:50%;
    padding:30px;
    padding-top:50px;
}
</style>