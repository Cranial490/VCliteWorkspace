<template>
	<div>
      <div>
        <b-form-checkbox v-model="checked" name="check-button" switch>
          ICICI escrow</b>
        </b-form-checkbox>
      </div>
      <div class="px-3 py-2">
        <b-list-group>
          <b-list-group-item><p class="billField">Username:<span class="spanText">{{user[0].username}}</span></p><p class="billData"></p></b-list-group-item>
          <b-list-group-item><p class="billField">PAN No:<span class="spanText">{{user[0].pan_no}}</span></p></b-list-group-item>
          <b-list-group-item><p class="billField">DPID:<span class="spanText">{{user[0].dpid}}</span></p></b-list-group-item>
          <b-list-group-item><p class="billField">Share:<span class="spanText">{{share.name}}</span></p></b-list-group-item>
          <b-list-group-item><p class="billField">ISI Number:<span class="spanText">None</span></p></b-list-group-item>
          <b-list-group-item><p class="billField">Price:<span class="spanText">{{price}}</span></p></b-list-group-item>
          <b-list-group-item><p class="billField">Quantity:<span class="spanText">{{quantity}}</span></p></b-list-group-item>
        </b-list-group>
        <h4 v-if="checked == false">Rs.{{ price*quantity }} + {{ brokerage*100 }}%</h4>
        <h4 v-if="checked == true">Rs.{{ price*quantity }} + {{ iciciBrokerage*100 }}%</h4>
        <h3>Rs.{{ totalAmountCalc() }}</h3>
      </div>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  components: {
  },
  data() {
    return {
      checked: false,
      brokerage: .015,
      iciciBrokerage: .02,
      totalAmount: 0,
      brokerageCalc: 0,
    }
  },
  props: [
    "user",
    "price",
    "quantity",
    "share",
  ],
  methods: {
    totalAmountCalc: function() {
      if(this.checked) {
        this.brokerageCalc = this.price * this.quantity * this.iciciBrokerage;
      }
      else {
        this.brokerageCalc = this.price * this.quantity * this.brokerage;
      }
      this.totalAmount = this.price * this.quantity + this.brokerageCalc;
      return this.totalAmount;
    }
  }
}
</script>