<template>
  
  <section id="filament-swap-page">
    <div v-if="isStart">
      <h2>No Filament Detected</h2>
      <p>It's time to change your filament.</p>
      <div>
        <button class="button block" v-on:click="setView('heat')">Start</button>
      </div>
    </div>
    <div v-if="isHeating">
      <h2>Replace Filament</h2>
      <p>
        Now, remove the remaining filament from the filament tube. 
        Replace the filament spool and feed new filament into filament tube up to the extruder.
      </p>
      <div>
        <button class="button block" v-on:click="startHeating()">Start Heating</button>
      </div>
      <div n-if="printerService.printer != null">
        <span>{{printerService.printer.temperatures.nozzle1.current}}/{{printerService.printer.temperatures.nozzle1.target}}</span>
        <span>{{printerService.printer.temperatures.nozzle2.current}}/{{printerService.printer.temperatures.nozzle2.target}}</span>
      </div>
    </div>
    <div v-if="isReady">
      <h2>Your hot-end is ready!</h2>
      <p>
        Click “Extrude” to feed your new filament. 
        Continue until you see filament extruding from the hot-end. 
        Once your hot-end is extruding, click “Resume”!
      </p>
      <div>
        <button class="button block" v-on:click="extrude(0, 100)">Extrude E1</button>
        <button class="button block" v-on:click="extrude(1, 100)">Extrude E2</button>
        <button class="button block" v-on:click="resumePrint()">Resume</button>
      </div>
    </div>
  </section>

</template>

<script>
  require('../../services/printer-service.js')

  export default {
    data () {
      return {
        printerService: printerws,
        view: 'start'
      }
    },
    methods: {
      setView: function (v) {
        this.view = v
      },
      startHeating: function () {
        this.printerService.setTemperatures({nozzle1:220})
        this.printerService.setTemperatures({nozzle2:220})
      },
      extrude: function (nid, length) {
        var rate = parseInt(this.printerService.printer.settings.presets.extrudeRate)
        this.printerService.unretractFilament(nid,length,rate)
      },
      resumePrint: function () {
        this.printerService.resumePrint()
      }
    },
    computed: {
      isStart: function () {
        return this.view === 'start'
      },
      isHeating: function () {
        return this.view === 'heat' && !this.isReady
      },
      isReady: function () {
        var toTemp = this.printerService.printer.temperatures.nozzle1.target > 200 || this.printerService.printer.temperatures.nozzle1.target  > 200 
        return this.view === 'heat' && toTemp
      }
    }
  }
</script>

<style>
#filament-swap-page{
  min-height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-content: center;
  padding: 0 1rem;
  color:#fff;
  margin-left:50px;
} 
#filament-swap-page h2{
  font-size: 1.8em;
  text-align: center;
  color:#fff;
  font-family: 'Exo', sans-serif;
  font-weight: 900;
  text-transform: uppercase;
}
#filament-swap-page p{
  text-align: center;
  font-size: 1.6em;
  width:50%;
  margin:40px auto;
}
#filament-swap-page div{
  text-align: center;
}
#filament-swap-page .button{
  margin:0 auto;
}
</style>
