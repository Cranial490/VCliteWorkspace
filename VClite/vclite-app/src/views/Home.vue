<template>
 <div class="content">
  <h1>Dashboard</h1>
  <b-container class="bv-example-row">
  	<input class="search-form" type="text" v-model="searchQuery" placeholder="Search" />	    
    <Table :shares="resultQuery"></Table>
  </b-container>
</div>
</template>

<script>
import axios from 'axios';
// import ListShare from '@/components/ListShare.vue'
import Table from '@/components/Table.vue'
import { mapState } from 'vuex'

export default {
  name: 'Home',
  data() {
  	return {
  		searchQuery: null,
  	}
  },
  components: {
  	Table
  },
  methods: {
  },
  created() {
    this.$store.dispatch('getUser');
    this.$store.dispatch('getShares');
  },
  computed : {
    resultQuery(){
      if(this.searchQuery){
      return this.$store.state.shares.filter((share)=>{
        return this.searchQuery.toLowerCase().split(' ').every(v => share.name.toLowerCase().includes(v))
      })
      }else{
        return this.$store.state.shares;
      }
    }
  }
}


</script>
<style>
.content {
	width:75%;
    float:right;
}
.search-form {
	float:right;
	margin: 10px;
	outline-width: 0;
	/*width: 10px%;*/
}
</style>