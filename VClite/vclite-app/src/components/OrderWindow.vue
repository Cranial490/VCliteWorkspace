<template>
  <b-container class="orderWindow">
  	<div>
      <!-- <TEST MODAL> -->
      <div>
       <b-modal ref="buy-modal" hide-footer title="Using Component Methods">
          <div class="d-block text-center">
            <h3>BUY</h3>
          </div>
          <b-button class="mt-3" variant="outline-info" block @click="BuyOrderConfirm()">Confirm Order</b-button>
          <b-button class="mt-3" variant="outline-danger" block @click="CancelOrder()">Cancel</b-button>
        </b-modal>
      </div>
      <div>
       <b-modal ref="sell-modal" hide-footer title="Using Component Methods">
          <div class="d-block text-center">
            <h3>SELL</h3>
          </div>
          <b-button class="mt-3" variant="outline-info" block @click="SellOrderConfirm()">Confirm Order</b-button>
          <b-button class="mt-3" variant="outline-danger" block @click="CancelOrder()">Cancel</b-button>
        </b-modal>
      </div>
      <!-- <MODAL TEST> -->

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
      modalShow: false,
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
      this.$refs['buy-modal'].show()
      var orderPrice = document.getElementById('buypriceId').value;
      this.$store.commit("updateCurrBuyPrice", orderPrice);

    },
    placeSellOrder() {
      this.$refs['sell-modal'].show()
      var orderPrice = document.getElementById('sellpriceId').value;
      this.$store.commit("updateCurrSellPrice", orderPrice);
    },
    BuyOrderConfirm() {
      this.$refs['buy-modal'].hide();
      alert("Buy Order Placed");
    },
    SellOrderConfirm() {
      this.$refs['sell-modal'].hide();
      alert("Sell Order Placed");
    },
    CancelOrder() {
      this.$refs['my-modal'].hide();
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
  .place-order {
    width: 50%;
    margin: 0 auto;
  }
  .closeBtn {
    width:10%;
  }

</style>