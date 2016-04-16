<script>
  // libs and services
  require('../services/printer-service.js')

  export default {
    components: {
    },
    data () {
      return {
        printerService: printerws,
        baseUrl: printerws.printer.connection.baseUrl,
        presets: printerws.printer.settings.presets
      }
    },
    methods: {
      connect: function () {
        this.printerService.connect()
      },
      setBaseUrl: function () {
        this.printerService.printer.connection.baseUrl = this.baseUrl
        // this.connect()
      }
    }
  }
</script>

<template>
  <section id="settings-page">

    <input class="url-input" placeholder="address for printer" v-model="baseUrl" v-on:blur="setBaseUrl">
    <div>
      <h3>extruder 1</h3>
      <div>
        <input class="preset-input" placeholder="extruder1 preset1 name" v-model="presets.nozzle1[0].name" v-on:blur="">
        <input class="preset-input" placeholder="extruder1 preset1 value" v-model="presets.nozzle1[0].value" v-on:blur="">
      </div>
      <div>
        <input class="preset-input" placeholder="extruder1 preset2 name" v-model="presets.nozzle1[1].name" v-on:blur="">
        <input class="preset-input" placeholder="extruder1 preset2 value" v-model="presets.nozzle1[1].value" v-on:blur="">
      </div>
    </div>
    <h3>extruder 2</h3>
    <div>
      <div>
        <input class="preset-input" placeholder="extruder2 preset1 name" v-model="presets.nozzle2[0].name" v-on:blur="">
        <input class="preset-input" placeholder="extruder2 preset1 value" v-model="presets.nozzle2[0].value" v-on:blur="">
      </div>
      <div>
        <input class="preset-input" placeholder="extruder2 preset2 name" v-model="presets.nozzle2[1].name" v-on:blur="">
        <input class="preset-input" placeholder="extruder2 preset2 value" v-model="presets.nozzle2[1].value" v-on:blur="">
      </div>
    </div>
    <h3>bed</h3>
    <div>
      <div>
        <input class="preset-input" placeholder="bed preset1 name" v-model="presets.bed[0].name" v-on:blur="">
        <input class="preset-input" placeholder="bed preset1 value" v-model="presets.bed[0].value" v-on:blur="">
      </div>
      <div>
        <input class="preset-input" placeholder="bed preset2 name" v-model="presets.bed[1].name" v-on:blur="">
        <input class="preset-input" placeholder="bed preset2 value" v-model="presets.bed[1].value" v-on:blur="">
      </div>
    </div>
    <h3>extrusion rate</h3>
    <div>
      <div>
        <input class="preset-input" placeholder="extrude rate" v-model="presets.extrudeRate" v-on:blur="">
      </div>
    </div>

  </section>
</template>

<style>

h2{
  text-align: center;
  font-family:'proxima_novalight';
}
.url-input{
  width: 100%;
  font-size: 1.5em;
  padding: 10px 10px;
  padding-bottom: 0px;
  padding-left: 0;
  color: #333;
  border: 0;
  border-bottom: 5px #ddd solid;
}
.preset-input{
  width: 20%;
  font-size: 1.5em;
  padding: 10px 10px;
  padding-bottom: 0px;
  padding-left: 0;
  color: #333;
  border: 0;
  border-bottom: 5px #ddd solid;
}
#settings-page{
} 
</style>

