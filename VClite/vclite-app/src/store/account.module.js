// actions for registering, login, logout user. 
// this triggers the actual backend api call in userService


import { userService } from '../_services'
import router from '../router'

const user = localStorage.getItem('user');

const state = user ? { status: { loggedIn: true }, user } : { status: {}, user: null };

const actions = {
	login({ dispatch, commit }, { username, password }) {
        commit('loginRequest', { username });
    
        userService.login(username, password)
            .then(
                user => {
                    commit('loginSuccess', user);
                    router.push('/');
                },
                error => {
                    alert("User credentials invalid")
                    commit('loginFailure', error);
                    dispatch('alert/error', error, { root: true });
                }
            );
    },
    logout({ commit }) {
        userService.logout();
        commit('logout');
    },

    handleFault({ commit }, error) {
        if(error.response.status == 401){
            commit('logout')
            userService.logout();
            location.reload(true);
        }
        else
            console.log(error.response.data)

    },

    register({ dispatch, commit }, user) {
        commit('registerRequest', user);
    
        userService.register(user)
            .then(
                user => {
                    //commit('registerSuccess', user);
                    router.push('/register2');
                    //setTimeout(() => {
                        // display success message after route change completes
                    //    dispatch('alert/success', 'Registration successful', { root: true });
                    //})
                },
                error => {
                    commit('registerFailure', error);
                    dispatch('alert/error', error, { root: true });
                }
            );
    },

    register2({ dispatch, commit }, user) {
        // check router history and based on that if it comes from order window do router.push(/history window)
        if(user.dpid == "" && user.pan_no == ""){
            console.log("pressed skip")
            commit('registerSuccess', user)
            dispatch('alert/success', 'Registration successful', { root: true });
            return
        }
        console.log("pressed continue")
        userService.register2(user)
        .then(
            user => {
                commit('registerSuccess', user)
                router.push('/register3')
                setTimeout(() => {
                    // display success message after route change completes
                    dispatch('alert/success', 'Registration successful', { root: true });
                })
            },
            error => {
                commit('registerFailure', error);
                dispatch('alert/error', error, { root: true });
            }
        );
    }
}

const mutations = {
	loginRequest(state, user) {
        state.status = { loggingIn: true };
        state.user = user;
    },
    loginSuccess(state, user) {
        state.status = { loggedIn: true };
        state.user = user;
    },
    loginFailure(state) {
        state.status = {};
        state.user = null;
    },
    logout(state) {
        state.status = {};
        state.user = null;
    },
    registerRequest(state, user) {
        state.status = { registering: true };
    },
    registerSuccess(state, user) {
        state.status = {};
    },
    registerFailure(state, error) {
        state.status = {};
    }
}

export const account = {
    namespaced: true,
    state,
    actions,
    mutations
}