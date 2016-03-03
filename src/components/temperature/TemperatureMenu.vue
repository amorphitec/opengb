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
        return this.target > (this.current + 10)
      }
    }
  }
</script>

<template>
  
  <div class="temperature-menu clear-fix" v-bind:class="{'is-open': isOpen}">
    <span class="label friendly-name" v-bind:class="{'is-heating': isHeating}">{{friendlyName}}</span>
    <div class="temperature-wrap">
      <div class="current-temp float-left" v-on:click="toggleOpen">{{current}}°C</div>
      <div class="target-temp float-left">
        <button class="button temp-select" v-bind:class="{'is-selected': target == 50}" v-if="tempId == 'bed'" v-on:click="setTemperature(50)">50°C</button>
        <button class="button temp-select" v-bind:class="{'is-selected': target == 180}" v-if="tempId != 'bed'" v-on:click="setTemperature(180)">PLA</button>
        <button class="button temp-select" v-bind:class="{'is-selected': target == 210}" v-if="tempId != 'bed'" v-on:click="setTemperature(210)">ABS</button>
      </div>
    </div>
  </div>

</template>


<style>
  .temperature-menu{
    margin-bottom:15px;
    border-radius:5px;
    padding:5px;
    background:rgba(0,0,0,.7);
    color:white;
    width:150px;
    overflow:hidden;
    font-size:2.5em;
    transition: width 0.5s;
  }
  .temperature-menu.is-open{
    width:300px;
  }
  .friendly-name{
    float:left;
    width:calc(100%);
    margin-right:50%;
  }
  .temperature-wrap{
    width:300px;
  }
  .current-temp{
    cursor:pointer;
    width:50%;
  }
  .target-temp{
    width:50%;
  }
  .button.temp-select{
    margin-top: 10px;
    opacity:.5;
  }
  .button.temp-select.is-selected{
    opacity:1;
  }

  .label.is-heating {
    -webkit-animation: beat  5s linear infinite;
    -moz-animation: beat 5s linear infinite;
    -ms-animation: beat 5s linear infinite;
    animation: beat 5s linear infinite;
    background: #c60f13;
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
