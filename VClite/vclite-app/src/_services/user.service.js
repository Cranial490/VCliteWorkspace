// Encloses All Backend API calls from here like logging in and out, registering, getting list of users, deletion of users etc.
import { authHeader } from '../_helpers/auth-header'
import axios from "axios";

export const userService = {
    login,
    logout,
    register,
    getAll,
    handleError,
    register2,
    //getById,
    //update
};



function login(username, password) {
    const requestOptions = {
        url: 'http://127.0.0.1:8000/auth/obtain_token/',
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        data: { username, password }
    };
    return axios(requestOptions)
        .then(response => {
            if(response.data.token){
                localStorage.setItem('user', response.data)
                localStorage.setItem('access_token', response.data.token)
            }
            console.log(response)
            return response.data
        })
        .catch(handleError)
}


function getAll() {
    const requestOptions = {
        url: 'http://127.0.0.1:8000/apiv0/user/',
        method: 'GET',
        headers: authHeader()
    };

    return axios(requestOptions)
    .then(response => {
        return response
    })
    .catch(handleError)
}


function logout() {
    // remove user from local storage to log user out
    localStorage.removeItem('user');
    localStorage.removeItem('access_token');
}

function register(user) {
    const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            data: user
            };

    return axios('http://127.0.0.1:8000/apiv0/register/', requestOptions)
    .then(res => {
        console.log(res)
        return Promise.resolve(res)
    })
    .catch(error => {
        console.log(error.response)
        if (error.response.status === 400) {
            console.log(error.response.data.username)
            //this.$refs.form.setErrors({
            //    "username": ['This username is already taken']
            //});
            if(error.response.data.username != undefined && error.response.data.username[0].includes("already exists")){
                        console.log("username already exists")
                        alert("Username already taken")
                }
            else if(error.response.data.phone_no != undefined && error.response.data.phone_no[0].includes("already exists")){
                        console.log("phone number already exists")
                        alert("Phone number already exists")
                }
            else if(error.response.data.email != undefined && error.response.data.email[0].includes("already exists")){
                        console.log("email already exists")
                        alert("Email already exists")
                }
        }
        return Promise.reject(error);
    })
}

function register2(user) {
    console.log("user = ", user)
    const requestOptions = {
        url: 'http://127.0.0.1:8000/apiv0/user/'+user.username+'/update_user',
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        data: {
            dpid: user.dpid,
            pan_no: user.pan_no
        }
    };
    return axios(requestOptions)
    .then(res => {
        console.log("res = ", res)
        return Promise.resolve(res)
    })
    .catch(error => {
        alert("DPID/Pan Number already exist")
        console.log("error = ", error.response)
        return Promise.reject(error);
    })
}


// Not being used 
function REFRESH_TOKEN() {
    return new Promise((resolve, reject) => {
        axios
        .post(`http://127.0.0.1:8000/auth/refresh_token/`, { 'token': localStorage.access_token })
        .then(response => {
            localStorage.removeItem('access_token')
            localStorage.setItem('access_token', response.data.token)
            resolve(response.data.token);
        })
        .catch(error => {
            reject(error);
        });
    });
}


// this method checks if the http response from the api is unauthorized and if yes will logout the user 
function handleResponse(response) {
    return response.text().then(text => {
        const data = text && JSON.parse(text);
        if (!response.ok) {
            if (response.status === 401) {
                // auto logout if 401 response returned from api
                logout();
                location.reload(true);
            }

            const error = (data && data.message) || response.statusText;
            return Promise.reject(error);
        }

        return data;
    });
}


function handleError(error) {
    console.log("error while logging in = ", error.response)
    if(error.response){
        switch(error.response.status) {
            case 401:

                this.logout()
                location.reload(true);
                break
            case 500:
                console.log(error.response.statusText)
                break
        }
    }
    return Promise.reject(error);
}


