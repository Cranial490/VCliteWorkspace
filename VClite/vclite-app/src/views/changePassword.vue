<template>
    <b-container class="loginBox">
        <div class="loginContent shadow">
            <ValidationObserver ref="form" v-slot="{ handleSubmit }">
            <b-form @submit.prevent="handleSubmit(onSubmit)">
                <h3>
                    Reset Password
                </h3>
                <br><br>
                <div class="col-10 form-group CommentBox">
                    <ValidationProvider rules="required|min:8|max:30|password:@confirm" v-slot="{ errors, valid }">
                        <b-input-group prepend="Password">
                        <b-form-input type="password" name="password" v-model="user.password" :state="errors[0] ? false : (valid ? true : null)" >
                        </b-form-input>
                        <b-form-invalid-feedback id="inputLiveFeedback">{{ errors[0] }}</b-form-invalid-feedback>
                        </b-input-group>
                        <!-- |password:@confirm -->
                    </ValidationProvider>
                </div>
                <div class="col-10 form-group CommentBox">
                    <ValidationProvider name="confirm" rules="required" v-slot="{ errors }">
                        <b-input-group prepend="Confirm Password">
                        <b-form-input type="password" name="confirmPassword" v-model="user.confirmPassword" :state="errors[0] ? false : (valid ? true : null)" >
                        </b-form-input>
                        <b-form-invalid-feedback id="inputLiveFeedback">{{ errors[0] }}</b-form-invalid-feedback>
                        </b-input-group>
                    </ValidationProvider>
                </div>
                <br><br>
                <div class="form-group">
                    <b-button pill variant="success" lg="4" class="pb-2" size="lg" type="submit">Save</b-button>
                </div>
            </b-form>
            </ValidationObserver>
        </div>
    </b-container>
</template>

<script>
import axios from "axios";
import router from '../router';

export default {
    data() {
        return {
            user: {
                password: '',
                confirmPassword: ''
            }
        }
    },
    created() {
        console.log("this.$route.params = ", this.$route.params)
    },
    methods: {
        onSubmit(){
            this.$refs.form.validate().then(valid => {
                if (valid) {
                    const requestOptions = {
                        url: 'http://127.0.0.1:8000/changePassword/'+this.$route.params.username+'/'+this.$route.params.validation_key+'/',
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        data: {
                            password: this.user.password
                        }
                    };
                    axios(requestOptions)
                    .then(response => {
                        console.log(response.data.message)
                        alert(response.data.message)
                        router.push('/changePassword2')
                    })
                }
            });
        }
    },
}
</script>


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
    width:70%;
    height:60%;
    padding:30px;
    padding-top:50px;
}
.CommentBox {
    margin:0 auto;
    margin-bottom: 10px;
}
</style>