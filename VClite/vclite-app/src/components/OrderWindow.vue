<template>
  <b-container class="orderWindow">
  	<div>
      <b-tabs :value="tabIndex" content-class="mt-3" fill>
        <b-tab title="Buy" active>
        <form>
          <h4>{{  }}</h4>
          <label>Price:</label>
          <input type="number" name="last" min=0 id="buypriceId" v-model="buy_price"><br/>
          <label>Qty:</label>
          <input type="number" name="email" min=1><br/>
          <b-button class="placer" block variant="success" size="lg" @click="placeBuyOrder()">BUY</b-button>
        </form>
      </b-tab>
      <b-tab title="Sell">
        <form>
          <h4>{{  }}</h4>
          <label>Price:</label>
          <input type="number" name="last" min=0 id="sellpriceId" v-model="sell_price"><br/>
          <label>Qty:</label>
          <input type="number" name="email" min=1><br/>
          <b-button class="placer" block variant="danger" size="lg" @click="placeSellOrder()">SELL</b-button>
        </form>
      </b-tab>
      </b-tabs>
    </div>
  </b-container>
</template>
<script>
// @ is an alias to /src

export default {
  data() {
    return {
      share_id: this.$route.params.shareid,
      orderQty: 0,
      buyOrderPrice: this.$store.state.currBuyPrice,
      sellOrderPrice: 0,
    }
  },
  components: {
  },
  created() {
    this.$store.dispatch('getShares'),
    this.$store.commit("resetPrice"),
    this.$store.commit("updateTransactionTypeIndex", 0)
  },
  methods: {
    filterShare() {
      return this.$store.state.shares.filter((share)=> {
        return share.id == this.$route.params.shareid
      })
    },
    getBuyPrice() {
      return this.$store.state.currBuyPrice;
    },
    getSellPrice() {
      return this.$store.state.currSellPrice;
    },
    placeBuyOrder() {
        var orderPrice = document.getElementById('buypriceId').value;
        alert(orderPrice);
        this.$store.commit("updateCurrBuyPrice", orderPrice);
        this.$bvToast.toast("Order Placed", {
          title: 'BUY',
          autoHideDelay: 3000,
        })
      },
    placeSellOrder() {
        var orderPrice = document.getElementById('sellpriceId').value;
        alert(orderPrice);
        this.$store.commit("updateCurrSellPrice", orderPrice);
        this.$bvToast.toast("Order Placed", {
          title: 'SELL',
          autoHideDelay: 3000,
        })
      }
  },
  computed: {
    buy_price: {
      get: function() {
      return this.$store.state.currBuyPrice;
    },
      set: function(newValue) {
        this.buyOrderPrice = newValue;
      }

  },
    sell_price: function() {
      return this.$store.state.currSellPrice;
    },
    tabIndex: function() {
      return this.$store.state.tabIndex;
    }
  },
}
</script>

<style>
  .orderWindow {
    /*width: 30%;*/
    border: 1px solid #f1f1f1;
    padding: 10px;
    border-radius: 25px;
  }

  .placer {
    margin-top: 10px;
  }

  label {
    display: inline-block;
    width:100px;
    text-align: left;
    margin-right: 5px;
}
</style>