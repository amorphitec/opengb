<script>
  require('../services/printer-service.js')
  import PositionInfo from '../components/position/PositionInfo.vue'
  import TemperatureInfo from '../components/temperature/TemperatureInfo.vue'
  import PositionControlCube from '../components/position/PositionControlCube.vue'
  import TemperatureMenu from '../components/temperature/TemperatureMenu.vue'

  export default {
    components: {
      PositionInfo,
      TemperatureInfo,
      PositionControlCube,
      TemperatureMenu
    },
    data () {
      return {
        printerService: printerws,
        view: 'movement'
      }
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
      },
      extrude: function (nid) {
        this.printerService.unretractFilament(nid,100,20)
      },
      retract: function (nid) {
        this.printerService.retractFilament(nid,100,20)
      }
    }
  }
</script>

<template>
  <section id="controls-page">

    <div class="slider-wrapper" v-bind:class="{'is-focus': isTemperature}">
      <div class="full-section">
        <div class="left-col">
          <temperature-info name="extruder 1" v-bind:value="printerService.printer.temperatures.nozzle1.current"></temperature-info>
          <temperature-info name="extruder 2" v-bind:value="printerService.printer.temperatures.nozzle2.current"></temperature-info>
          <temperature-info name="bed" v-bind:value="printerService.printer.temperatures.bed.current"></temperature-info>
          <button class="" v-on:click="setView('temperature')">more</button>
        </div>
        <div class="right-col">
          <temperature-menu 
            friendly-name="Heated Bed - Target"
            temp-id="bed"
            v-bind:current="printerService.printer.temperatures.bed.target"
            v-bind:target="printerService.printer.temperatures.bed.target"
            >
          </temperature-menu>
          <temperature-menu 
            friendly-name="Extruder 1 - Target"
            temp-id="nozzle1"
            v-bind:current="printerService.printer.temperatures.nozzle1.target"
            v-bind:target="printerService.printer.temperatures.nozzle1.target"
            >
          </temperature-menu>
          <temperature-menu 
            friendly-name="Extruder 2 - Target"
            temp-id="nozzle2"
            v-bind:current="printerService.printer.temperatures.nozzle2.target"
            v-bind:target="printerService.printer.temperatures.nozzle2.target"
            >
          </temperature-menu>
          <button class="button" v-on:click="extrude(0)">feed Extruder 1</button>
          <button class="button" v-on:click="retract(0)">retract Extruder 1</button>
          <button class="button" v-on:click="extrude(1)">feed Extruder 2</button>
          <button class="button" v-on:click="retract(1)">retract Extruder 2</button>
        </div>
      </div>
    </div>

    <div class="slider-wrapper" v-bind:class="{'is-focus': isMovement}" >
      <div class="full-section">
        <div class="left-col">
          <position-info name="x" v-bind:value="printerService.printer.position.x"></position-info>
          <position-info name="y" v-bind:value="printerService.printer.position.y"></position-info>
          <position-info name="z" v-bind:value="printerService.printer.position.z"></position-info>
          <button class="" v-on:click="setView('movement')">more</button>
        </div>
        <div class="right-col">
          <div id="position-cube">
            <position-control-cube></position-control-cube>
          </div>
        </div>
      </div>
    </div>

    <div class="slider-wrapper" v-bind:class="{'is-focus': isTerminal}" >
      <div class="full-section">
        <div class="left-col">
          <button class="" v-on:click="setView('terminal')">more</button>
        </div>
        <div class="right-col">
        </div>
      </div>
    </div>
  </section>
</template>

<style>
  h2{
    text-align: center;
    font-family: 'proxima_novalight';
  }
  #controls-page{
    min-height: 100%;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-content: center;
  }
  #position-cube{
    position: relative;
    width:500px;
    height:500px;
  } 
  .slider-wrapper{
    flex: 0;
    transition:all 1s;
  }
  .slider-wrapper.is-focus{
    flex: 8;
    /*min-width: 70%;*/
  }
  .full-section{
    min-height: 100%;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-content: center;
  }
  .left-col{
    padding:10px;
  }
  .right-col{
    position:relative;
    width:0;
    overflow:hidden;
    transition:all 0.2s;
  }
  .slider-wrapper.is-focus .right-col{
    width:100%;
  }
</style>