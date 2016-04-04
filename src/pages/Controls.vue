<script>
  require('../services/printer-service.js')
  import PositionInfo from '../components/position/PositionInfo.vue'
  import TemperatureInfo from '../components/temperature/TemperatureInfo.vue'
  import PositionControlCube from '../components/position/PositionControlCube.vue'
  import TemperatureMenu from '../components/temperature/TemperatureMenuAdv.vue'

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
        view: 'movement',
        extrudeLength: 100
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
      extrude: function (nid, length) {
        this.printerService.unretractFilament(nid,length,5)
      },
      retract: function (nid, length) {
        this.printerService.retractFilament(nid,length,5)
      },
      increaseExtrudeLength: function () {
        console.log('increasing el')
        this.extrudeLength += 10
      },
      decreaseExtrudeLength: function () {
        console.log('decreasing el')
        this.extrudeLength = this.extrudeLength < 10 ? 0 : this.extrudeLength - 10
      }
    }
  }
</script>

<template>
  <section id="controls-page">

    <div class="slider-wrapper" v-bind:class="{'is-focus': isTemperature}">
      <div class="full-section dark">
        <div class="left-col">
          <h2>heat</h2>
          <temperature-info name="extruder 1" v-bind:value="printerService.printer.temperatures.nozzle1.current"></temperature-info>
          <temperature-info name="extruder 2" v-bind:value="printerService.printer.temperatures.nozzle2.current"></temperature-info>
          <temperature-info name="bed" v-bind:value="printerService.printer.temperatures.bed.current"></temperature-info>
          <button class="" v-on:click="setView('temperature')">more</button>
        </div>
        <div class="right-col">
          <div class="extrude-length">
            <span>extrude <input v-model="extrudeLength" />mm</span>
            <span class="block float-right" style="margin-top:20px;">
              <button class="button temp-select" v-on:click="increaseExtrudeLength">+</button>
              <button class="button temp-select" v-on:click="decreaseExtrudeLength">-</button>
            </span>
          </div>
          <div class="temp-menu-wrapper">
            <span class="block">
              <temperature-menu 
                friendly-name="Extruder 1 - Target"
                temp-id="nozzle1"
                v-bind:current="printerService.printer.temperatures.nozzle1.target"
                v-bind:target="printerService.printer.temperatures.nozzle1.target"
                >
              </temperature-menu>
            </span>
            <span class="block top">
              <button class="button block" v-on:click="extrude(0, extrudeLength)">Extrude</button>
              <button class="button block" v-on:click="retract(0, extrudeLength)">Retract</button>
            </span>
          </div>
          <div class="temp-menu-wrapper">
            <span class="block">
              <temperature-menu 
                friendly-name="Extruder 2 - Target"
                temp-id="nozzle2"
                v-bind:current="printerService.printer.temperatures.nozzle2.target"
                v-bind:target="printerService.printer.temperatures.nozzle2.target"
                >
              </temperature-menu>
            </span>
            <span class="block top">
              <button class="button block" v-on:click="extrude(1, extrudeLength)">Extrude</button>
              <button class="button block" v-on:click="retract(1, extrudeLength)">Retract</button>
            </span>
          </div>
          <div class="temp-menu-wrapper">
            <span class="block">
              <temperature-menu 
                friendly-name="Heated Bed - Target"
                temp-id="bed"
                v-bind:current="printerService.printer.temperatures.bed.target"
                v-bind:target="printerService.printer.temperatures.bed.target"
                >
              </temperature-menu>
            </span>
          </div>
        </div>
      </div>
    </div>

    <div class="slider-wrapper" v-bind:class="{'is-focus': isMovement}" >
      <div class="full-section">
        <div class="left-col">
          <h2>move</h2>
          <position-info name="x" v-bind:value="printerService.printer.position.x"></position-info>
          <position-info name="y" v-bind:value="printerService.printer.position.y"></position-info>
          <position-info name="z" v-bind:value="printerService.printer.position.z"></position-info>
          <button class="" v-on:click="setView('movement')">more</button>
        </div>
        <div class="right-col">
          <div class="top-padding"></div>
          <div id="position-cube">
            <position-control-cube></position-control-cube>
          </div>
        </div>
      </div>
    </div>

  </section>
</template>

<style>
  .extrude-length{
    width:275px;
    margin: 0 10px;
    text-align: right;
    font-family: 'Exo', sans-serif;
    font-weight: 700;
    text-transform: uppercase;
  }
  .extrude-length input{
    line-height: 65px;
    padding: 0 5px;
    width: 90px;
    background: transparent;
    color: white;
    border: 0;
    text-align: right;
    font-size: 2em;
    font-family: 'Exo', sans-serif;
    font-weight: 200;  
  }
  .left-col h2{
    text-align: center;
    font-family: 'Exo', sans-serif;
    font-weight: 700;
    text-transform: uppercase;
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
    min-width: 175px;
    transition:all 1s;
    overflow: hidden;
  }
  .slider-wrapper.is-focus{
    flex: 8;
    /*min-width: 70%;*/
  }
  .full-section{
    min-height: 100vh;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-content: center;
  }
  .left-col{
    padding:10px;
    min-width:175px;
    text-align: center;
  }
  .full-section.dark{
    background: #333;
    color:white;
  }
  .full-section.dark h2{
    color:#ddd;
  }
  .right-col{
    position:relative;
    /*width:0;*/
  }
  .callout{
    /*this should be in a different file.*/
    padding:0!important;
  }
  .button.block{
    display: block;
    height: 35px;
  }
  .temp-menu-wrapper{
    position: relative;
    height: 80px;
    margin-bottom: 10px;
  }
  .top{
    position: absolute;
    top:2px;
    right:-100px;
  }
</style>