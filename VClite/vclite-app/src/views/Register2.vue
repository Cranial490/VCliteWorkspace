<template>
    <b-container class="RegisterBox2">
    <div>
        <b-jumbotron>
        <ValidationObserver ref="form2" v-slot="{ handleSubmit }">
            <b-form @submit.prevent="handleSubmit(onSubmit)">
                <div class="col-6 form-group CommentBox">
                    <ValidationProvider rules="required|min:16|max:16" v-slot="{ errors, valid }">
                        <b-input-group prepend="DPID">
                        <b-form-input type="number" v-model="user.dpid" name="dpid" :state="errors[0] ? false : (valid ? true : null)">
                        </b-form-input>
                        <b-form-invalid-feedback id="inputLiveFeedback">{{ errors[0] }}</b-form-invalid-feedback>
                        </b-input-group>
                    </ValidationProvider>
                </div>
                <div class="col-6 form-group CommentBox">
                    <ValidationProvider rules="required|min:10|max:10" v-slot="{ errors, valid }">
                        <b-input-group prepend="Pan Number">
                        <b-form-input type="text" v-model="user.pan_no" name="panNo" :state="errors[0] ? false : (valid ? true : null)"></b-form-input>
                        </b-input-group>
                        <b-form-invalid-feedback id="inputLiveFeedback2">{{ errors[0] }}</b-form-invalid-feedback>
                        </b-input-group>
                    </ValidationProvider>
                </div>
                <div class="form-group">
                    <router-link class="btn btn-link" v-if="status.loggedIn == undefined" @click.native="onSkipRegister" to="/register3">Skip</router-link>
                    <b-button pill variant="info" lg="4" class="pb-2" type="submit">Continue</b-button>
                </div>
            </b-form>
        </ValidationObserver>
    </b-jumbotron>
    </div>
</b-container>
</template>

<script>
// @click.native="onSkipRegister"
// class="btn btn-link"
// "!status.loggedIn ? 'onSkipRegister' : ''"
import { mapState, mapActions } from 'vuex'
import { bus } from '../main'
import axios from 'axios';

export default {
    data () {
        return {
            user: {
                username: '',
                dpid: '',
                pan_no: '',
            },
        }
    },
    created() {
        this.user.username = localStorage.getItem('Username')
        console.log("username = ", this.user.username)
    },
    computed: {
        ...mapState('account', ['status']),
    },
    methods: {
        ...mapActions('account', ['register', 'register2']),
        onSkipRegister() {
            this.register2(this.user)
        },

        onSubmit() {
            this.$refs.form2.validate().then(valid => {
                if (valid) {
                    console.log("this.status.loggedIn = ", this.status.loggedIn)
                    if(this.status.loggedIn){
                        this.user.username = localStorage.getItem('userName')
                    }
                    this.register2(this.user);
                }
            });
        }
    }
};
</script>

<style>

.CommentBox {
    margin:0 auto;
    margin-bottom: 30px;
}
</style>