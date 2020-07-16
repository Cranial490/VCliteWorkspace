import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  	shares: [],
  	currBuyPrice: 0,
  	currSellPrice: 0,
  	orderType: "",
  	tabIndex: 0,
  },
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
  	updateTransactionTypeIndex(state, index) {
  		state.tabIndex = index;
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
  	}
  },
  modules: {
  }
})