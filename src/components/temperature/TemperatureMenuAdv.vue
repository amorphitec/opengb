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
      },
      increaseTemperature: function  () {
        this.setTemperature( parseInt(this.target) + 1 )
      },
      decreaseTemperature: function () {
        this.setTemperature( parseInt(this.target) - 1 )
      },
      getPresetName: function (i) {
        return this.printerService.printer.settings.presets[this.tempId][i].name
      },
      getPresetTemp: function (i) {
        return this.printerService.printer.settings.presets[this.tempId][i].value
      },
      isTargetTemp: function (i) {
        return this.target == this.getPresetTemp(i)
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
      },
      currentText: function () {
        var text = this.current > 30 ? parseInt(this.current) + '°C' : 'OFF'
        return text
      }
    }
  }
</script>

<template>
  
  <div class="temperature-menu-adv clear-fix is-open" v-bind:class="{'is-on':isOn}">
    <div class="temperature-wrap">
      <span class="block float-left">
        <button class="button temp-select" v-bind:class="{'is-selected': isTargetTemp(0)}" v-on:click="setTemperature(getPresetTemp(0))">{{getPresetName(0)}}</button>
        <button class="button temp-select" v-bind:class="{'is-selected': isTargetTemp(1)}" v-on:click="setTemperature(getPresetTemp(1))">{{getPresetName(1)}}</button>
      </span>
      <span class="target-temp block">
        <h3 class="label">target</h3>
        <div class="current-temp" v-on:click="toggleOpen">{{currentText}}</div>
      </span>
      <span class="block float-right">
        <button class="button temp-select" v-on:click="increaseTemperature">+</button>
        <button class="button temp-select" v-on:click="decreaseTemperature">-</button>
      </span>
    </div>
  </div>

</template>


<style>
  .block{
    display:inline-block;
    margin:0 10px;
  }
  .temperature-menu-adv{
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
    font-weight: 200;
    height: 80px;
  }
  .temperature-menu-adv.is-open{
    width:275px;
  }
  .temperature-menu-heading{
    width:300px;    
  }
  .label{
    float:left;
    width:50%;
    background: transparent!important;
    text-align: center;
    padding-bottom:0!important;
    font-family: 'Exo', sans-serif;
    font-weight: 700;
    text-transform: uppercase;
  }
  .temperature-menu-adv .temperature-wrap{
    width:100%;
    text-align: center;
  }
  .current-temp{
    cursor:pointer;
  }
  .current-temp{
    cursor:pointer;
  }
  .target-temp{
    width:auto;
    text-align: center;
  }
  .temperature-menu-adv .button.temp-select{
    margin: 0px;
    padding: 0.5em 1em;
    background: #ddd;
    color:#777;
    opacity: 0.5;
    display: block;
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

  .temperature-menu-adv.is-on {
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
