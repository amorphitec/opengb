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

    <div class="full-section">

      <div class="full-width">

        <div id="settings-heading">
          <h2>Settings</h2>
        </div>

        <div class="settings-section">
          <h3 class="settings-subheading">websockets</h3>
          <input class="url-input" placeholder="address for printer" v-model="baseUrl" v-on:blur="setBaseUrl">
        </div>

        <div class="settings-section two-col">

          <div class="half-width">
            <h3>heat pre-settings</h3>

            <div class="heat-setting">
              <h4>Extruder 1</h4>
              <div class="heat-setting-inputs">
                <div>
                  <input class="preset-input" placeholder="extruder1 preset1 name" v-model="presets.nozzle1[0].name" v-on:blur="">
                  <input class="preset-input" placeholder="extruder1 preset1 value" v-model="presets.nozzle1[0].value" v-on:blur="">
                </div>
                <div>
                  <input class="preset-input" placeholder="extruder1 preset2 name" v-model="presets.nozzle1[1].name" v-on:blur="">
                  <input class="preset-input" placeholder="extruder1 preset2 value" v-model="presets.nozzle1[1].value" v-on:blur="">
                </div>
              </div>
            </div>

            <div class="heat-setting">
              <h4>Extruder 2</h4>
              <div class="heat-setting-inputs">
                <div>
                  <input class="preset-input" placeholder="extruder2 preset1 name" v-model="presets.nozzle2[0].name" v-on:blur="">
                  <input class="preset-input" placeholder="extruder2 preset1 value" v-model="presets.nozzle2[0].value" v-on:blur="">
                </div>
                <div>
                  <input class="preset-input" placeholder="extruder2 preset2 name" v-model="presets.nozzle2[1].name" v-on:blur="">
                  <input class="preset-input" placeholder="extruder2 preset2 value" v-model="presets.nozzle2[1].value" v-on:blur="">
                </div>
              </div>
            </div>

            <div class="heat-setting">
              <h4>Bed</h4>
              <div class="heat-setting-inputs">
                <div>
                  <input class="preset-input" placeholder="bed preset1 name" v-model="presets.bed[0].name" v-on:blur="">
                  <input class="preset-input" placeholder="bed preset1 value" v-model="presets.bed[0].value" v-on:blur="">
                </div>
                <div>
                  <input class="preset-input" placeholder="bed preset2 name" v-model="presets.bed[1].name" v-on:blur="">
                  <input class="preset-input" placeholder="bed preset2 value" v-model="presets.bed[1].value" v-on:blur="">
                </div>
              </div>
            </div>
          </div>

          <div class="half-width">
            <h3>heat pre-settings</h3>

            <div class="extrusion-setting">
              <h4>Extrusion Rate</h4>
              <div class="extrusion-setting-inputs">
                <div>
                  <input class="preset-input" placeholder="extrude rate" v-model="presets.extrudeRate" v-on:blur="">
                </div>
              </div>
            </div>

          </div>

        </div>

      </div>

    </div>

  </section>

</template>

<style>
.full-width{
  width:100%;
}
.half-width{
  width:50%;
}
#settings-heading{
  width:100%;
}
#settings-heading h2{
  text-align: left;
  font-family: 'Exo', sans-serif;
  font-weight: 700;
  text-transform: uppercase;  
  color:#ccc;
  margin: 5px 0;
}
.settings-section {
  margin-bottom: 30px;
}
.settings-section.two-col{
  min-height: 100%;
  display: -webkit-box;
  display: -webkit-flex;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-orient: horizontal;
  -webkit-box-direction: normal;
  -webkit-flex-direction: row;
  -ms-flex-direction: row;
  flex-direction: row;
  -webkit-box-pack: start;
  -webkit-justify-content: flex-start;
  -ms-flex-pack: start;
  justify-content: flex-start;
  -webkit-align-content: center;
  -ms-flex-line-pack: center;
  align-content: center;
}
.settings-section h3{
  text-align: left;
  font-family: 'Exo', sans-serif;
  font-weight: 900;
  text-transform: uppercase;  
  color:#000;
  font-size:1em;
  margin:0;
}
.heat-setting, .extrusion-setting{
  min-height: 100%;
  display: -webkit-box;
  display: -webkit-flex;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-orient: horizontal;
  -webkit-box-direction: normal;
  -webkit-flex-direction: row;
  -ms-flex-direction: row;
  flex-direction: row;
  -webkit-box-pack: start;
  -webkit-justify-content: flex-start;
  -ms-flex-pack: start;
  justify-content: flex-start;
  -webkit-align-content: center;
  -ms-flex-line-pack: center;
  align-content: center;
}
.heat-setting h4, .extrusion-setting h4{
  width:66%;
  line-height: 2em;
}
.heat-setting-inputs{
  min-height: 100%;
  display: -webkit-box;
  display: -webkit-flex;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-orient: horizontal;
  -webkit-box-direction: normal;
  -webkit-flex-direction: column;
  -ms-flex-direction: column;
  flex-direction: column;
  -webkit-box-pack: start;
  -webkit-justify-content: flex-start;
  -ms-flex-pack: start;
  justify-content: flex-start;
  -webkit-align-content: center;
  -ms-flex-line-pack: center;
  align-content: center;
}
.heat-setting-inputs input{
  width:40%;
}
.extrusion-setting-inputs input{
  width:100%;
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
  min-height: 100%;
  display: -webkit-box;
  display: -webkit-flex;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-orient: horizontal;
  -webkit-box-direction: normal;
  -webkit-flex-direction: row;
  -ms-flex-direction: row;
  flex-direction: row;
  -webkit-box-pack: start;
  -webkit-justify-content: flex-start;
  -ms-flex-pack: start;
  justify-content: flex-start;
  -webkit-align-content: center;
  -ms-flex-line-pack: center;
  align-content: center;
  padding: 0 1rem;
} 
</style>

