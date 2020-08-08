import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import createPersistedState from "vuex-persistedstate";

import { alert } from './alert.module'
import { account } from './account.module'
import { authHeader } from '../_helpers/auth-header'
Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  	shares: [],
    loggedUser: [],
  	currBuyPrice: 0,
  	currSellPrice: 0,
  	orderType: "",
    userLog: [],
    // orders: [],
  },
  plugins: [createPersistedState()],
  mutations: {
  	updateShareList(state, shares) {
  		state.shares = shares;
  	},
  	updateCurrBuyPrice(state, price) {
  		state.currBuyPrice = price;
  	},
  	updateCurrSellPrice(state, price) {
  		state.currSellPrice = price;
  	},
  	resetPrice(state) {
  		state.currBuyPrice = 0;
  		state.currSellPrice = 0;
  	},
    updateLogUser(state,userLog) {
      state.userLog = userLog;
    },
    // updateOrders(state, orders) {
    //   state.orders = orders;
    // }
  },
  actions: {
  	getShares({commit}) {
  		axios.get("http://127.0.0.1:8000/apiv0/shares/")
  		.then(res => res.data)
  		.then(shares => {
  			commit('updateShareList', shares)
  		})
  		.catch(err => console.log(err));
  	},
    getUser({commit}) {
      axios.get("http://127.0.0.1:8000/apiv0/user/", {headers: authHeader()})
      .then(res => res.data)
      .then(userLog => {
        commit('updateLogUser', userLog)
      })
      .catch(err => console.log(err));
    },
    // getOrders({commit}) {
    //   axios.get("http://127.0.0.1:8000/apiv0/order/", {headers: authHeader()})
    //   .then(res => res.data)
    //   .then(orders => {
    //     commit('updateOrders', orders)
    //   })
    //   .catch(err => console.log(err));
    // },
  },
  modules: {
    alert,
    account
  }
})