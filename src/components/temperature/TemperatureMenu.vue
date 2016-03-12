<script>
  require('../../services/printer-service.js')
  export default {
    data () {
      return {
        isOpen: false,
        tempTemperature: '',
        printerService: printerws
      }
    },
    props: {
      tempId: '',
      friendlyName: '',
      current: '',
      target: '',
      state: ''
    },
    methods: {
      toggleOpen: function () {
        this.isOpen = !this.isOpen
      },
      setTemperature: function (temp) {
        var obj = {}
        if (this.target != temp) {
          obj[this.tempId] = temp
        } else {
          obj[this.tempId] = 1
      }
        this.printerService.setTemperatures(obj)
      }
    },
    computed:{
      isHeating: function () {
        var test = parseFloat(this.target) > (parseFloat(this.current) + 10)
        return test
      },
      isOn: function () {
        var test = parseFloat(this.target) > 40
        return test
      }
    }
  }
</script>

<template>
  
  <div class="temperature-menu clear-fix" v-bind:class="{'is-open': isOpen, 'is-on':isOn}">
    <div class="temperature-menu-heading">
      <span class="label friendly-name" v-bind:class="{'is-heating': isHeating}">{{friendlyName}}</span>
      <span class="label friendly-name">prepare</span>
    </div>
    <div class="temperature-wrap">
      <div class="current-temp float-left" v-on:click="toggleOpen">{{current}}°C</div>
      <div class="target-temp float-left">
        <button class="button temp-select" v-bind:class="{'is-selected': target == 50}" v-if="tempId == 'bed'" v-on:click="setTemperature(50)">PLA</button>
        <button class="button temp-select" v-bind:class="{'is-selected': target == 60}" v-if="tempId == 'bed'" v-on:click="setTemperature(60)">ABS</button>
        <button class="button temp-select" v-bind:class="{'is-selected': target == 180}" v-if="tempId != 'bed'" v-on:click="setTemperature(180)">PLA</button>
        <button class="button temp-select" v-bind:class="{'is-selected': target == 210}" v-if="tempId != 'bed'" v-on:click="setTemperature(210)">ABS</button>
      </div>
    </div>
  </div>

</template>


<style>
  .temperature-menu{
    margin-bottom:8px;
    border-radius:5px;
    padding:5px 0px;
    background:#22f;
    color:white;
    width:150px;
    overflow:hidden;
    font-size:2em;
    transition: width 0.5s;
    font-family: 'Exo', sans-serif;
    font-weight: 700;
  }
  .temperature-menu.is-open{
    width:300px;
  }
  .temperature-menu-heading{
    width:300px;    
  }
  .friendly-name{
    float:left;
    width:50%;
    background: transparent!important;
    text-align: center;
    padding-bottom:0!important;
  }
  .temperature-wrap{
    width:300px;
    text-align: center;
  }
  .current-temp{
    cursor:pointer;
    width:50%;
  }
  .target-temp{
    width:50%;
  }
  .button.temp-select{
    margin: 0px;
    padding: 0.5em 1em;
    background: #ddd;
    color:#777;
    opacity: 0.5;
  }
  .button.temp-select:hover, .button.temp-select:focus{
    background: #ccc!important;
  }
  .button.temp-select.is-selected{
    background: #a60003!important;
    color:#fff;
    opacity: 1;
  }
  .button.temp-select.is-selected:hover, .button.temp-select.is-selected:focus{
    background: #900!important;
  }

  .temperature-menu.is-on {
    background: #c60f13;
  }

  .label.is-heating {
    -webkit-animation: beat  5s linear infinite;
    -moz-animation: beat 5s linear infinite;
    -ms-animation: beat 5s linear infinite;
    animation: beat 5s linear infinite;
  }
  
  @keyframes beat {
    0% {
      opacity: 0.7;
    }
    50% {
      opacity: 1;
    }
    100% {
      opacity: 0.7;
    }
  }

  @-moz-keyframes beat {
    0% {
      opacity: 0.7;
    }
    50% {
      opacity: 1;
    }
    100% {
      opacity: 0.7;
    }
  }

  @-webkit-keyframes beat {
    0% {
      opacity: 0.7;
    }
    50% {
      opacity: 1;
    }
    100% {
      opacity: 0.7;
    }
  }

  @-ms-keyframes beat {
    0% {
      opacity: 0.7;
    }
    50% {
      opacity: 1;
    }
    100% {
      opacity: 0.7;
    }
  }

</style>
