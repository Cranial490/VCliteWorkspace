<template>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-5">
                <div class="card card-default">
                    <div class="card-header">Forgot your Password?</div>
                    <div class="card-body">
                        <ValidationObserver ref="form" v-slot="{ handleSubmit }">
                            <form @submit.prevent="handleSubmit(onSubmit)">
                                <div class="form-group text-xsmall">
                                    <ValidationProvider rules="required|email" v-slot="{ errors, valid }">
                                    <b-input-group prepend="Email">
                                        <b-form-input type="text" name="Email" v-model="user.email" :state="errors[0] ? false : (valid ? true : null)">
                                        </b-form-input>
                                        <b-form-invalid-feedback id="inputLiveFeedback">{{ errors[0] }}</b-form-invalid-feedback>
                                    </b-input-group>
                                    </ValidationProvider>
                                </div>
                                <!--<div class="form-group text-xsmall">
                                    <ValidationProvider rules="required|min:10|max:10" v-slot="{ errors, valid }">
                                    <b-input-group prepend="PAN">
                                        <b-form-input type="text" name="pan_no" v-model="user.pan_no" :state="errors[0] ? false : (valid ? true : null)">
                                        </b-form-input>
                                        <b-form-invalid-feedback id="inputLiveFeedback">{{ errors[0] }}</b-form-invalid-feedback>
                                    </b-input-group>
                                    </ValidationProvider>
                                </div>-->
                                <br><br>
                                <div class="form-group text-xsmall">
                                    <b-button squared variant="info" lg="4" size="lg" class="pb-2" type="submit">Reset</b-button>
                                    <br>
                                    <router-link to="/login" class="btn btn-link">« Back to Login</router-link>
                                </div>
                            </form>
                        </ValidationObserver>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import { mapState, mapActions } from 'vuex'
import axios from "axios";
import router from '../router';

export default {
    data() {
        return {
            user: {
                email: '',
                pan_no: ''
            }
        }
    },
    computed: {

    },
    methods: {
        onSubmit() {
            this.$refs.form.validate().then(valid => {
                if (valid) {
                    // send reset password request
                    const resetPasswordRequest = {
                        url: 'http://127.0.0.1:8000/auth/reset-password/',
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        data: {
                            email: this.user.email
                        }
                    };
                    axios(resetPasswordRequest)
                    .then(response => {
                        console.log("mail sent")
                        console.log(response)
                        router.push('/forgot2')
                    })
                    .catch(error => {
                        switch(error.response.status) {
                            case 400:
                                alert("Bad Request, No such email registered")
                                console.log("Bad Request, No such email registered")
                                break
                            case 401:
                                alert("Invalid Credentials")
                                break
                            case 500:
                                console.log(error.response.statusText)
                                alert(error.response.statusText)
                                break
                        }
                    })
                    
                }
            });
        }
    },
    components: {

    },
}


</script>
