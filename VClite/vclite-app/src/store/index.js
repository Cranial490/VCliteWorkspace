import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import createPersistedState from "vuex-persistedstate";

import { alert } from './alert.module'
import { account } from './account.module'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    validation_status: { buyOrderValidated: false, sellOrderValidated: false },
  	shares: [],
  	currBuyPrice: 0,
  	currSellPrice: 0,
  	orderType: "",
  },
  plugins: [createPersistedState()],
  mutations: {
  	updateShareList(state, shares) {
  		state.shares = shares;
  	},
  	updateCurrBuyPrice(state, price) {
  		state.currBuyPrice = price;
      state.validation_status.buyOrderValidated = true;
  	},
  	updateCurrSellPrice(state, price) {
  		state.currSellPrice = price;
      state.validation_status.sellOrderValidated = true;
      //console.log("sell  price = ", price)
  	},
  	resetPrice(state) {
  		state.currBuyPrice = 0;
  		state.currSellPrice = 0;
  	}
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
    CurrSellPriceRequest({commit}, {price, quantity}) {
      console.log("inside currsellpricerequest")
      console.log("price = ", price)
      console.log("quantity = ", quantity)
      if(price > 0 && quantity >0){
        console.log("sell  price = ", price)
        commit('updateCurrSellPrice', price)
      }
    },
    CurrBuyPriceRequest({commit}, {price, quantity}) {
      if(price > 0 && quantity >0){
        commit('updateCurrBuyPrice', price)
      }

    },
  },
  modules: {
    alert,
    account
  }
})