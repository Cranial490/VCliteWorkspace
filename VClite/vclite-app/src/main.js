// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'

import App from './App'
import router from './router'
import store from './store'
import Vuex from 'vuex'
import axios from 'axios'

import './Validators/index';
import { ValidationProvider } from 'vee-validate';
import { ValidationObserver } from 'vee-validate';

import BootstrapVue from 'bootstrap-vue/dist/bootstrap-vue.esm';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import 'bootstrap/dist/css/bootstrap.css';
import Carousel3d from 'vue-carousel-3d';

Vue.use(Vuex)

Vue.config.productionTip = false
Vue.use(BootstrapVue);
Vue.use(Carousel3d);

//Event bus for component communication 
export const bus = new Vue();

Vue.component('ValidationObserver', ValidationObserver)
Vue.component('ValidationProvider', ValidationProvider)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
