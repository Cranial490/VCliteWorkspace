<template>
    <b-container class="RegisterBox1">
    <div>
        <div>
            
                <b-modal
                    id="phone-number-modal"
                    ref="phone_modal"
                    title="Verify Phone Number"
                    no-close-on-esc=true
                    no-close-on-backdrop=true
                    hide-footer
                    no-stacking
                >
                <span>
                    You will receive an OTP on this number
                </span>
                <!--<ValidationObserver ref="form" v-slot="{ handleSubmit }">-->
                <!-- ref="form"-->
                <form @submit.stop.prevent="handleSubmit(onSubmitModal)">
                    <div class="col-8 form-group CommentBox">
                    <b-input-group prepend="+91">
                    <b-form-input :state="digitState" type="tel" min="10" max="10" required aria-placeholder="10 digit Mobile" name="phone_no" v-model="user.phone_no">
                    </b-form-input>
                    <b-form-invalid-feedback id="inputLiveFeedback">Mobile Number should be 10 digits</b-form-invalid-feedback>
                    </b-input-group>
                    </div>
                    <span v-if="message === true" STYLE="color: green; font-size: 10pt">
                        OTP sent on your mobile
                    </span>
                    <div>
                        <b-button class="mt-3" native-type="submit" size="sm" variant="outline-info" block @click="onSubmitModal()">Send</b-button>
                    </div>
                    <div v-if="message === true">
                        <b-button class="mt-2" native-type="submit" size="sm" variant="outline-success" block @click="onNextModal()">Continue</b-button>
                    </div>
                </form>
                <!--</ValidationObserver>-->
                </b-modal>
            
        </div>
        <div>
                <b-modal
                    id="otp-verify-modal"
                    ref="otp_modal"
                    title="Verify Phone Number"
                    no-close-on-esc=true
                    no-close-on-backdrop=true
                    ok-only
                    @ok="handleOk"
                    button-size="md"
                    ok-title="Confirm"
                    no-stacking
                >
                <span>
                    Confirm your OTP
                </span>
                <form ref="form" @submit.stop.prevent="handleSubmit(onOTPModal)">
                    <div class="col-6 form-group CommentBox">
                    <b-input-group prepend="OTP">
                    <b-form-input :state="OTPState" id="FormOTP"  type="text" pattern="\d*" aria-placeholder="OTP" maxlength="6" name="OTP" v-model="phone.OTP" >
                    </b-form-input>
                    </b-input-group>
                    </div>
                    <span v-if="OTPVerified === 2" STYLE="color: green; font-size: 10pt">
                        OTP verified successfully!
                    </span>
                    <span v-if="OTPVerified === 3" STYLE="color: red; font-size: 10pt">
                        {{ errorMessage }}
                    </span>
                </form>
                </b-modal>
        </div>
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
                <b-form-input type="tel" name="phone_no" v-model="user.phone_no" :state="errors[0] ? false : (valid ? true : null)" >
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
//v-if="message === true" STYLE="color: green; font-size: 10pt"
// ok-only
// button-size="md"
// @ok="handleOKay"
// ok-title="Continue"
import { mapState, mapActions } from 'vuex'
import axios from "axios";
import { bus } from '../main'
import { userService } from '../_services'

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
                phone: {
                    OTP: '',
                },
                message: false,
                session_token: '',
                OTPVerified: 1,
                Duplicates: false,
                errorMessage: 'Invalid OTP, Try again',
        }
    },
    computed: {
        ...mapState('account', ['status']),
        digitState() {
            return this.user.phone_no.length == 10 ? true : false
        },
        OTPState() {
            return this.phone.OTP.length == 6 ? true: false
        },

    },
    methods: {
        ...mapActions('account', ['register']),

        checkifUserAlreadyExists() {
            const params = {
                username: this.user.username,
                phone_no: this.user.phone_no,
                email: this.user.email
            };
            const headers = {
                'Content-Type': 'application/json'
            }
            return axios.get("http://127.0.0.1:8000/apiv0/register/duplicates/", {params, headers})
            .then(res => {
                console.log(res)
                this.Duplicates = false
                return Promise.resolve(res)
            })
            .catch(error => {
                console.log("error = ", error)
                console.log("error = ", error.response.data.message)
                this.Duplicates = true
                alert(error.response.data.message)
                return Promise.reject(error.response.data.message)
            })
        },

        onSubmit() {
            this.$refs.form.validate().then(async (valid) => {
                if (valid) {
                     await this.checkifUserAlreadyExists()
                    .then(response => {
                        console.log(response)
                    })
                    .catch(error => {
                        console.log(error)
                    })
                    //console.log("username = ", this.user.username)
                    //let userName = this.user.username
                    //bus.$emit('Username', userName)
                    if(this.Duplicates == false){
                        localStorage.setItem('Username', this.user.username)
                        this.$refs['phone_modal'].show();
                    }
                    //this.register(this.user);
                }
            });
        },

        sendOTP() {
            const requestOptions = {
                url: 'http://127.0.0.1:8000/OTP/phone/register',
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                data: {
                    phone_number: "+91"+String(this.user.phone_no),
                },
            }
            return axios(requestOptions)
            .then(response => {
                if(response.status == 200){
                    this.session_token = response.data.session_token
                    return Promise.resolve("Session Token received")
                }
                else{
                    this.session_token = null
                    return Promise.reject("Session Token not received")
                }
            })
        },


        onSubmitModal() {
            this.$refs.form.validate().then(async(valid) => {
                if(valid){
                    await this.sendOTP()
                    .then(response => {
                        console.log(response)
                    })
                    .catch(error => {
                        console.log(error)
                    })
                    this.message = true
                    return
                }
                console.log("invalid")
                return
            })
        },
        onNextModal() {
            if(this.message){
                console.log("message = ", this.message)
                this.$refs['otp_modal'].show();
            }
        },

        verifyOTP() {
            const requestOptions = {
                url: 'http://127.0.0.1:8000/OTP/phone/verify',
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                data: {
                    phone_number: "+91"+String(this.user.phone_no),
                    session_token: this.session_token,
                    security_code: this.phone.OTP,
                },
            }
            return axios(requestOptions)
            .then(response => {
                if(response.status == 200){
                    console.log("OTP is valid")
                    this.OTPVerified = 2
                    //return Promise.resolve("OTP is verified")
                }
            })
            .catch(error => {
                this.OTPVerified = 3
                this.errorMessage = error.response.data.non_field_errors[0]
                console.log(error.response.data.non_field_errors[0])
                if(error.response.data.non_field_errors[0] == "Security code has expired")
                    location.reload(true)
                //return Promise.reject("Invalid OTP")
            })
        },

        async onOTPModal() {
            await this.verifyOTP()
            if(this.OTPVerified === 2){
                this.register(this.user)
            }
            else if(this.OTPVerified === 3){
                //document.getElementById('FormOTP').reset();
                return
            }
        },
        handleOk(bvModalEvt) {
            bvModalEvt.preventDefault()
            console.log("inside handleOk")
            if(this.phone.OTP.length > 0)
                this.onOTPModal()
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