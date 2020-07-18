<template>
  <b-container class="orderWindow">
  	<div>
      <!-- <TEST MODAL> -->
      <div>
       <b-modal ref="buy-modal" hide-footer title="BUY Order Summary">
          <div class="d-block text-center">
            <h3>Invoice</h3>
            <OrderSummary 
            :user="'None'"
            :price="$store.state.currBuyPrice"
            :quantity="buyOrderQty"
            :share="filterShare()[0]"
            ></OrderSummary>
          </div>
          <b-button class="mt-3" variant="outline-info" block @click="BuyOrderConfirm()">Confirm Order</b-button>
        </b-modal>
      </div>
      <div>
       <b-modal ref="sell-modal" hide-footer title="SELL Order Summary">
          <div class="d-block text-center">
            <h3>Invoice</h3>
            <OrderSummary 
            :user="'None'"
            :price="$store.state.currSellPrice"
            :quantity="sellOrderQty"
            :share="filterShare()[0]"
            ></OrderSummary>
          </div>
          <b-button class="mt-3" variant="outline-info" block @click="SellOrderConfirm()">Confirm Order</b-button>
        </b-modal>
      </div>
      <!-- <MODAL TEST> -->

      <b-tabs :value="tabIndex" content-class="mt-3" fill>
        <b-tab title="Buy" active>
        <form>
          <label>Price:</label>
          <input ref="buyPriceInput" type="number" name="last" min=0 id="buypriceId" v-model="buy_price"><br/>
          <label>Qty:</label>
          <input ref="buyQtyInput" type="number" name="email" min=1><br/>
          <b-button class="placer" block variant="success" size="lg" @click="placeBuyOrder()">BUY</b-button>
        </form>
      </b-tab>
      <b-tab title="Sell">
        <form>
          <label>Price:</label>
          <input ref="sellPriceInput" type="number" name="last" min=0 id="sellpriceId" v-model="sell_price"><br/>
          <label>Qty:</label>
          <input ref="sellQtyInput" type="number" name="email" min=1><br/>
          <b-button class="placer" block variant="danger" size="lg" @click="placeSellOrder()">SELL</b-button>
        </form>
      </b-tab>
      </b-tabs>
    </div>
  </b-container>
</template>
<script>
// @ is an alias to /src
import OrderSummary from '@/components/OrderSummary.vue'
export default {
  data() {
    return {
      share_id: this.$route.params.shareid,
      buyOrderQty: 0,
      sellOrderQty: 0,
      buyOrderPrice: this.$store.state.currBuyPrice,
      sellOrderPrice: 0,
      modalShow: false,
      status: 'not_accepted',
    }
  },
  components: {
    OrderSummary,
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
      this.buyOrderQty = this.$refs['buyQtyInput'].value;
      // console.log(this.orderQty);
      this.$refs['buy-modal'].show();
      var orderPrice = document.getElementById('buypriceId').value;
      this.$store.commit("updateCurrBuyPrice", orderPrice);

    },
    placeSellOrder() {
      this.sellOrderQty = this.$refs['sellQtyInput'].value;
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
    margin-right: 0px;
  }
  .place-order {
    width: 50%;
    margin: 0 auto;
  }
  .closeBtn {
    width:10%;
  }
  .billField{
  text-align: left;
}
.billData {
  text-align: right;
}
.spanText {
  float:right;
}
.checkbox-1{
  float: left;
}

</style>