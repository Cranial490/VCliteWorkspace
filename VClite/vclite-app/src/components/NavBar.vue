<template>
	<b-navbar toggleable="lg" type="light" variant="light">
    <b-navbar-brand href="#">VC<sup>lite</sup></b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item to="/">Home</b-nav-item>
        <b-nav-item to="/positions">Positions</b-nav-item>
        <b-nav-item to="/orders">Orders</b-nav-item>
        <b-nav-item to="/explore">Explore</b-nav-item>
        <b-nav-item to="/about">About</b-nav-item>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-item-dropdown right>
          <!-- Using 'button-content' slot -->
          <template v-slot:button-content>
            <em><b-avatar variant="success" text="PP"></b-avatar></em>
          </template>
          <b-dropdown-item :to="{ path: '/profile' }">Profile</b-dropdown-item>
          <b-dropdown-item href="#">Support</b-dropdown-item>
          <b-dropdown-item :to="{ path: '/login' }">Sign Out</b-dropdown-item>
        </b-nav-item-dropdown>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</template>
<script>
// @ is an alias to /src

export default {
  components: {
  }
}
</script>