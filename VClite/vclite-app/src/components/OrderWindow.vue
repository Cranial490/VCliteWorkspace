<template>
  <b-container class="orderWindow">
    <div>
      <!-- <TEST MODAL> -->
      <div>
        <ValidationObserver ref="form-modal" v-slot="{ handleSubmit }">
       <b-modal ref="buy-modal" hide-footer title="BUY Order Summary" @ok="handleSubmit(BuyOrderConfirm)">
          <div class="d-block text-center">
            <h3>Invoice</h3>
            <OrderSummary 
            :user="$store.state.userLog"
            :price="$store.state.currBuyPrice"
            :quantity="buyOrderQty"
            :share="filterShare()[0]"
            ></OrderSummary>
          </div>
          <b-button class="mt-3" native-type="submit" variant="outline-info" block @click="BuyOrderConfirm()">Confirm Order</b-button>
        </b-modal>
        </ValidationObserver>
      </div>
      <div>
        <ValidationObserver ref="form-modal" v-slot="{ handleSubmit }">
        <b-modal ref="sell-modal" hide-footer title="SELL Order Summary" @ok="handleSubmit(SellOrderConfirm)">
          <div class="d-block text-center">
            <h3>Invoice</h3>
            <OrderSummary 
            :user="$store.state.userLog"
            :price="$store.state.currSellPrice"
            :quantity="sellOrderQty"
            :share="filterShare()[0]"
            ></OrderSummary>
          </div>
          <b-button class="mt-3" variant="outline-info" block @click="SellOrderConfirm()">Confirm Order</b-button>
        </b-modal>
        </ValidationObserver>
      </div>
      <!-- <MODAL TEST> -->
      <b-tabs v-model="tabIndex" content-class="mt-3" fill>
        <b-tab title="Buy" active>
        <ValidationObserver ref="form" v-slot="{ handleSubmit }">
          <form @submit.prevent="handleSubmit(placeBuyOrder)">
            <h3 v-if="filterShare().length > 0">{{ filterShare()[0].share_name }}</h3>
            <div class="form-group">
              <ValidationProvider rules="required|minValue:1" v-slot="{ errors, valid }" >
                <b-input-group prepend="Price:">
                <b-form-input ref="buyPriceInput" type="number" name="s-price" id="buypriceId" v-model="buyOrderPrice" :state="errors[0] ? false : (valid ? true : null)"><br/>
                </b-form-input>
                <b-form-invalid-feedback id="inputLiveFeedback">{{ errors[0] }}</b-form-invalid-feedback>
              </b-input-group>
              </ValidationProvider>
            </div>
            <div class="form-group">
              <ValidationProvider rules="required|minValue:1" v-slot="{ errors, valid }" >
                <b-input-group prepend="Qty:">
                <b-form-input ref="buyQtyInput" type="number" name="s-qty" v-model="buyOrderQty" :state="errors[0] ? false : (valid ? true : null)" ><br/>
                  </b-form-input>
                <b-form-invalid-feedback id="inputLiveFeedback">{{ errors[0] }}</b-form-invalid-feedback>
                </b-input-group>
              </ValidationProvider>
            </div>
            <div class="form-group">
              <b-button class="placer" block variant="success" size="lg" type="submit">BUY</b-button>
            </div>
          </form>
        </ValidationObserver>
      </b-tab>
      <b-tab title="Sell">
        <ValidationObserver ref="form" v-slot="{ handleSubmit }">
          <form @submit.prevent="handleSubmit(placeSellOrder)">
            <h3 v-if="filterShare().length > 0">{{ filterShare()[0].share_name }}</h3>
            <div class="form-group">
              <ValidationProvider rules="required|minValue:1" v-slot="{ errors, valid }" >
                <b-input-group prepend="Price:">
                <b-form-input ref="sellPriceInput" type="number" name="s-price" id="sellpriceId" v-model="sellOrderPrice" :state="errors[0] ? false : (valid ? true : null)" ><br/>
                </b-form-input>
                <b-form-invalid-feedback id="inputLiveFeedback">{{ errors[0] }}</b-form-invalid-feedback>
                </b-input-group>
              </ValidationProvider>
            </div>
            <div class="form-group">
              <ValidationProvider rules="required|minValue:1" v-slot="{ errors, valid }" >
                <b-input-group prepend="Qty:">
                <b-form-input ref="sellQtyInput" type="number" name="s-qty" v-model="sellOrderQty" :state="errors[0] ? false : (valid ? true : null)"><br/>
                </b-form-input>
                <b-form-invalid-feedback id="inputLiveFeedback">{{ errors[0] }}</b-form-invalid-feedback>
                </b-input-group>
              </ValidationProvider>
            </div>
            <div class="form-group">
              <b-button class="placer" block variant="danger" size="lg" type="submit">SELL</b-button>
            </div>
          </form>
        </ValidationObserver>
      </b-tab>
      </b-tabs>
    </div>
  </b-container>
</template>
<script>
// @ is an alias to /src
import OrderSummary from '@/components/OrderSummary.vue'
import { bus } from '../main'
import axios from 'axios'
import { authHeader } from '../_helpers/auth-header'
import { mapState, mapActions } from 'vuex'

export default {
  data() {
    return {
      share_id: this.$route.params.shareid,
      buyOrderQty: '',
      sellOrderQty: '',
      buyOrderPrice: '',//this.$store.state.currBuyPrice,
      sellOrderPrice: '',
      modalShow: false,
      status: 'not_accepted',
      tabIndex: 0,
      isLoaded: false,
      userData: this.$store.state.userLog,
    }
  },
  components: {
    OrderSummary,
  },
  created() {
    this.$store.commit("resetPrice")
  },
  methods: {
    ...mapActions('account', ['register']),
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
      console.log("dpid = ", this.userData[0].dpid)
      console.log("pan_no = ", this.userData[0].pan_no)
      if(this.userData[0].dpid == null || this.userData[0].pan_no == null){
        console.log("localStorage username = ", localStorage.getItem('userName'))
        localStorage.setItem('userName', this.userData[0].username)
        console.log("localStorage username = ", localStorage.getItem('userName'))
        localStorage.setItem('disableSkip', true)
        this.$router.push('/register2')
        return
      }
      console.log("inside buy order confirm")
      this.$refs['buy-modal'].hide();
      this.$bvToast.toast(`Bought @ Rs.${this.$store.state.currBuyPrice} per share`, {
          title: 'Buy Order Placed',
          variant: 'success',
          autoHideDelay: 3000,
        })
      console.log("Executing Buy Order");
      const axios_request = {
        url: 'http://127.0.0.1:8000/apiv0/order/execute/',
        method: 'POST',
        headers: authHeader(),
        data: {
          price: this.$store.state.currBuyPrice,
          quantity: this.buyOrderQty,
          updated_quantity: this.buyOrderQty,
          user: this.userData[0].username, 
          share: this.filterShare()[0].name,
          order_type: 'BUY'
        }
      };
        axios(axios_request)
        .then(response => (this.info = response.data))
    },
    SellOrderConfirm() {
      console.log("dpid = ", this.userData[0].dpid)
      console.log("pan_no = ", this.userData[0].pan_no)
      if(this.userData[0].dpid == null || this.userData[0].pan_no == null){
        console.log("localStorage username = ", localStorage.getItem('userName'))
        localStorage.setItem('userName', this.userData[0].username)
        console.log("localStorage username = ", localStorage.getItem('userName'))
        localStorage.setItem('disableSkip', true)
        this.$router.push('/register2')
        return
      }
      console.log("inside sell order confirm")
      this.$refs['sell-modal'].hide();
      this.$bvToast.toast(`Sold @ Rs.${this.$store.state.currSellPrice} per share`, {
          title: 'Sell Order Placed',
          variant: 'danger',
          autoHideDelay: 3000,
        })
      console.log("Executing Sell Order");
      const axios_request = {
        url: 'http://127.0.0.1:8000/apiv0/order/execute/',
        method: 'POST',
        headers: authHeader(),
        data: {
          price: this.$store.state.currSellPrice,
          quantity: this.sellOrderQty,
          updated_quantity: this.sellOrderQty,
          user: this.userData[0].username, 
          share: this.filterShare()[0].name,
          order_type: 'SELL'
        }
      };
        axios(axios_request)
        .then(response => (this.info = response.data))
    },
  },
  computed: {
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