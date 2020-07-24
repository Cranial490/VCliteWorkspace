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
      <b-tabs v-model="tabIndex" content-class="mt-3" fill>
        <b-tab title="Buy" active>
        <form>  <!--@submit.prevent="placeBuyOrder"-->
          <h3 v-if="filterShare().length > 0">{{ filterShare()[0].share_name }}</h3>
          <label>Price:</label>
          <input ref="buyPriceInput" type="number" name="s-price" min=0 id="buypriceId" v-model="buy_price"><br/>
          <label>Qty:</label>
          <input ref="buyQtyInput" type="number" name="s-qty" min=1 ><br/>
          <b-button class="placer" block variant="success" size="lg" @click="placeBuyOrder()">BUY</b-button>
        </form>
      </b-tab>
      <b-tab title="Sell">
        <form @submit.prevent="placeSellOrder"> <!-- @submit.prevent="placeSellOrder"-->
          <h3 v-if="filterShare().length > 0">{{ filterShare()[0].share_name }}</h3>
          <div class="form-group">
            <label>Price:</label>
            <input ref="sellPriceInput" type="number" name="s-price" min=0 id="sellpriceId" v-model="sell_price" ><br/>
            <div v-show="submitted && !sellOrderPrice" class="invalid-feedback">Invalid Price</div>
          </div>
          <div class="form-group">
            <label>Qty:</label>
            <input ref="sellQtyInput" type="number" name="s-qty" min=1 :class="{ 'is-invalid': submitted && !this.sellOrderQty}"><br/>
            <div v-show="submitted && !sellOrderQty" class="invalid-feedback">Invalid Quantity</div>
          </div>
          <div class="form-group">
            <b-button class="placer" block variant="danger" size="lg" @click="placeSellOrder()" :disabled="!validation_status.sellOrderValidated">SELL</b-button>
          </div>
        </form>
      </b-tab>
      </b-tabs>
    </div>
  </b-container>
</template>
<!--@click="placeSellOrder()"-->
<script>
// @ is an alias to /src
import OrderSummary from '@/components/OrderSummary.vue'
import { bus } from '../main'
import axios from 'axios'
import { mapState } from 'vuex'

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
      tabIndex: 0,
      isLoaded: false,
      submitted: false,
    }
  },
  components: {
    OrderSummary,
  },
  created() {
    this.$store.commit("resetPrice")
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
      this.submitted = true
      this.buyOrderQty = this.$refs['buyQtyInput'].value;
      this.$refs['buy-modal'].show();
      var orderPrice = document.getElementById('buypriceId').value;
      this.$store.commit("updateCurrBuyPrice", orderPrice);

    },
    placeSellOrder() {
      this.submitted = true
      this.sellOrderQty = this.$refs['sellQtyInput'].value;
      this.$refs['sell-modal'].show()
      var sellQty = this.sellOrderQty
      var orderPrice = document.getElementById('sellpriceId').value;
      console.log("1 orderPrice = ", orderPrice)
      console.log("1 orderQty = ", this.sellOrderQty)
      //const {sellOrderPrice, sellOrderQty} = this;
      console.log("2 orderPrice = ", orderPrice)
      console.log("2 orderQty = ", this.sellOrderQty) //6
      this.$store.dispatch("CurrSellPriceRequest", {orderPrice, sellQty})
      //this.$store.commit("updateCurrSellPrice", orderPrice);
    },
    BuyOrderConfirm() {
      this.$refs['buy-modal'].hide();
      this.$bvToast.toast(`Bought @ Rs.${this.$store.state.currBuyPrice} per share`, {
          title: 'Buy Order Placed',
          variant: 'success',
          autoHideDelay: 3000,
        })
    },
    SellOrderConfirm() {
      this.$refs['sell-modal'].hide();
      this.$bvToast.toast(`Sold @ Rs.${this.$store.state.currSellPrice} per share`, {
          title: 'Sell Order Placed',
          variant: 'danger',
          autoHideDelay: 3000,
        })
    },
  },
  computed: {
    ...mapState(['validation_status', 'currBuyPrice', 'currSellPrice']),
    buy_price: function(){
      return this.$store.state.currBuyPrice;
    },
    sell_price: function() {
      return this.$store.state.currSellPrice;
    },
  },
  mounted () {
    bus.$on('updateTabIndex', (data) => {
      this.tabIndex = data;
    })
  }
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