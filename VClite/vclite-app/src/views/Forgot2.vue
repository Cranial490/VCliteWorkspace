<template>
    <b-container class="loginBox">
        <div class="loginContent shadow">
            <form>
                <h1>
                    E-mail Sent
                </h1>
                <br><br>
                <h4>
                    An e-mail has been sent to you with the password reset link.
                </h4>
                <br>
                <router-link to="/login" class="btn btn-link">« Back to Login</router-link>
            </form>
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