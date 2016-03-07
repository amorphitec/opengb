<script>
  require('../services/printer-service.js')
  import PositionInfo from '../components/position/PositionInfo.vue'
  import TemperatureMenu from '../components/temperature/TemperatureMenu.vue'

  export default {
    components: {
      PositionInfo,
      TemperatureMenu
    },
    data () {
      return {
        printerService: printerws,
        view: 'movement'
      }
    },
    ready: function () {
      console.log('childNodes: ', this.$el.childNodes)
    },
    computed: {
      isMovement: function () {
        return this.view === 'movement'
      },
      isTemperature: function () {
        return this.view === 'temperature'
      },
      isTerminal: function () {
        return this.view === 'terminal'
      },
      isNotPrinting: function () {
        var s = this.printerService.printer.state
        return s != 'EXECUTING' && s != 'PAUSED'
      }
    },
    methods: {
      setView: function (v) {
        this.view = v
      },
      homePrinter: function () {
        this.printerService.homePrintHead({x:true,y:true,z:true})
      }
    }
  }
</script>

<template>
  <section id="controls-page">

    <div class="slider-wrapper" v-bind:class="{'is-focus': isTemperature}">
    </div>

    <div class="slider-wrapper" v-bind:class="{'is-focus': isMovement}" >
    </div>

    <div class="slider-wrapper">
    </div>
  </section>
</template>

<style>
  h2{
    text-align: center;
    font-family: 'proxima_novalight';
  }
  #control-page{
    min-height: 100%;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-content: center;
  } 
  .slider-wrapper{
    flex: 0;
  }
  .slider-wrapper.is-focus{
    flex: 8;
    min-width: 70%;
  }
</style>