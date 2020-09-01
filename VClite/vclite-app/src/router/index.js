import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register1 from '../views/Register1.vue'
import Register2 from '../views/Register2.vue'
import Register3 from '../views/Register3.vue'
import Forgot from '../views/Forgot.vue'
import Forgot2 from '../views/Forgot2.vue'
import changePassword from '../views/changePassword.vue'
import changePassword2 from '../views/changePassword2.vue'

Vue.use(VueRouter)

  const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  { 
    path: '/register1',
    name: 'Register1',
    component: Register1 
  },
  { 
    path: '/register2',
    name: 'Register2',
    component: Register2
  },
  { 
    path: '/register3',
    name: 'Register3',
    component: Register3
  },
  { 
    path: '/forgot',
    name: 'Forgot',
    component: Forgot
  },
  { 
    path: '/forgot2',
    name: 'Forgot2',
    component: Forgot2
  },
  { 
    path: '/changePassword/:username/:validation_key/',
    name: 'changePassword',
    component: changePassword
  },
  { 
    path: '/changePassword2',
    name: 'changePassword2',
    component: changePassword2
  },
  {
    path: '/positions',
    name: 'Positions',
    component: () => import('@/views/Positions.vue')
  },
  {
    path: '/orders',
    name: 'Orders',
    component: () => import('../views/Orders.vue')
  },
  {
    path: '/terminal/:shareid',
    name: 'Terminal',
    component: () => import('../views/Terminal.vue')
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue')
  },
  {
    path: '/explore',
    name: 'Explore',
    component: () => import('../views/Explore.vue')
  },
  {
    path: '/edit',
    name: 'Edit',
    component: () => import('../views/EditUser.vue')
  },
  {
    path: '/faq',
    name: 'FAQ',
    component: () => import('../views/FAQ.vue')
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue')
  },
  { path: '*', redirect: '/' }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  //console.log("to.path = ", to.path)
  // redirect to login page if not logged in and trying to access a restricted page
  const publicPages = ['/login', '/register1', '/register2', '/register3', '/forgot', '/forgot2', '/changePassword', '/changePassword2'];
  const authRequired = !(publicPages.includes(to.path) || to.path.includes('changePassword'));
  const loggedIn = localStorage.getItem('user');
  console.log("authrequired = ", authRequired)
  if (authRequired && !loggedIn) {
    return next('/login');
  }

  next();
})

export default router
