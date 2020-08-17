<template>
    <b-container class="RegisterBox1">
    <div>
        <b-jumbotron header="Register">
        <ValidationObserver ref="form" v-slot="{ handleSubmit }">
        <b-form @submit.prevent="handleSubmit(onSubmit)">
            <div class="col-6 form-group CommentBox">
                <ValidationProvider rules="required|min:3|alpha" v-slot="{ errors, valid }">
                    <b-input-group prepend="First Name">
                    <b-form-input type="text" name="firstName" v-model="user.first_name" :state="errors[0] ? false : (valid ? true : null)" >
                    </b-form-input>
                    <b-form-invalid-feedback id="inputLiveFeedback">{{ errors[0] }}</b-form-invalid-feedback>
                    </b-input-group>
                </ValidationProvider>
            </div>
            <div class="col-6 form-group CommentBox">
                <ValidationProvider rules="required|min:3|alpha" v-slot="{ errors, valid }">
                    <b-input-group prepend="Last Name">
                    <b-form-input type="text" name="lastName" v-model="user.last_name" :state="errors[0] ? false : (valid ? true : null)" >
                    </b-form-input>
                    <b-form-invalid-feedback id="inputLiveFeedback">{{ errors[0] }}</b-form-invalid-feedback>
                    </b-input-group>
                </ValidationProvider>
            </div>
            <div class="col-6 form-group CommentBox">
                <ValidationProvider rules="required" v-slot="{ errors, failedRules, valid }">
                    <b-input-group prepend="Username">
                    <b-form-input type="text" name="username" v-model="user.username" :state="errors[0] ? false : (valid ? true : null)" >
                    </b-form-input>
                    <b-form-invalid-feedback id="inputLiveFeedback">{{ errors[0] }}</b-form-invalid-feedback>
                    </b-input-group>
                </ValidationProvider>
            </div>
            <div class="col-6 form-group CommentBox">
                <ValidationProvider rules="required|min:10|max:10" v-slot="{ errors, failedRules, valid }">
                <b-input-group prepend="Phone No">
                <b-form-input type="number" name="phone_no" v-model="user.phone_no" :state="errors[0] ? false : (valid ? true : null)" >
                </b-form-input>
                <b-form-invalid-feedback id="inputLiveFeedback">{{ errors[0] }}</b-form-invalid-feedback>
                </b-input-group>
                </ValidationProvider>
            </div>
            <div class="col-6 form-group CommentBox">
                <ValidationProvider rules="required|email" v-slot="{ errors, failedRules, valid }">
                <b-input-group prepend="Email">
                <b-form-input type="text" name="email" v-model="user.email" :state="errors[0] ? false : (valid ? true : null)" >
                </b-form-input>
                <b-form-invalid-feedback id="inputLiveFeedback">{{ errors[0] }}</b-form-invalid-feedback>
                </b-input-group>
                </ValidationProvider>
            </div>
            <div class="col-6 form-group CommentBox">
                <ValidationProvider rules="required|min:8|max:30|password:@confirm" v-slot="{ errors, valid }">
                    <b-input-group prepend="Password">
                    <b-form-input type="password" name="password" v-model="user.password" :state="errors[0] ? false : (valid ? true : null)" >
                    </b-form-input>
                    <b-form-invalid-feedback id="inputLiveFeedback">{{ errors[0] }}</b-form-invalid-feedback>
                    </b-input-group>
                </ValidationProvider>
            </div>
            <div class="col-6 form-group CommentBox">
                <ValidationProvider name="confirm" rules="required" v-slot="{ errors }">
                    <b-input-group prepend="Confirm Password">
                    <b-form-input type="password" name="confirmPassword" v-model="user.confirmPassword" :state="errors[0] ? false : (valid ? true : null)" >
                    </b-form-input>
                    <b-form-invalid-feedback id="inputLiveFeedback">{{ errors[0] }}</b-form-invalid-feedback>
                    </b-input-group>
                </ValidationProvider>
            </div>
            <div class="form-group">
                <b-button pill variant="info" lg="4" class="pb-2" size="lg" type="submit">Continue</b-button>
                <router-link to="/login" class="btn btn-link">Cancel</router-link>
            </div>
            </b-form>
        </ValidationObserver>
    </b-jumbotron>
    </div>
</b-container>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import axios from "axios";
import { bus } from '../main'

// status.registering instead of this.flag
export default {
    data () {
        return {
                user: {
                    first_name: '',
                    last_name: '',
                    username: '',
                    phone_no: '',
                    email: '',
                    password: '',
                    confirmPassword: '',
                },
        }
    },
    computed: {
        ...mapState('account', ['status'])
    },
    methods: {
        ...mapActions('account', ['register']),
        onSubmit() {
            this.$refs.form.validate().then(valid => {
                if (valid) {
                    //console.log("username = ", this.user.username)
                    localStorage.setItem('Username', this.user.username)
                    //let userName = this.user.username
                    //bus.$emit('Username', userName)
                    this.register(this.user);
                }
            });
        }
    },
    components: {
        
    }
};
</script>

<style>

.CommentBox {
    margin:0 auto;
    margin-bottom: 10px;
}
</style>