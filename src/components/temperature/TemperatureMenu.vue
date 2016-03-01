<script>
  require('../../services/printer-service.js')
  export default {
    data () {
      return {
        isOpen: false,
        tempTemperature: ''
      }
    },
    props: {
      id: '',
      friendlyName: '',
      current: '',
      target: '',
      state: ''
    },
    methods: {
      toggleOpen: function () {
        this.isOpen = !this.isOpen
      },
      updateTemperature: function () {
      }
    }
  }
</script>

<template>
  
  <div class="temperature-menu clear-fix" v-bind:class="{'is-open': isOpen}">
    <span class="label friendly-name">{{friendlyName}}</span>
    <div class="temperature-wrap">
      <div class="current-temp float-left" v-on:click="toggleOpen">{{current}}°C</div>
      <div class="target-temp float-left">{{target}}°C</div>
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
</style>
