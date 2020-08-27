<template>
  <b-container class="bv-example-row">
    <table class="table table-hover">
    <thead>
      <tr>
        <th>Instrument</th>
        <th>Price</th>
        <th>Quantity</th>a
      </tr>
    </thead>
    <tbody>
      <tr v-for="share in shares" :key="share.id" @click="fetchDepth(share.id)">
        <td>{{ share.name }}</td>
        <td>{{ share.ltp }}</td>
        <td>{{ share.quantity }}</td>
      </tr>
    </tbody>
  </table>                  
  </tr>
</b-container>
</template>

<script>
// @ is an alias to /src

export default {
  props: [
    "shares"
  ],
  methods: {
  fetchDepth(id) {
    this.$router.push({ name: 'Terminal', params: { shareid:id } });
    }
  }
}
</script>