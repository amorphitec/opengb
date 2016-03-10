<script>
  // libs and services
  require('../services/printer-service.js')

  export default {
    components: {
    },
    data () {
      return {
        printerService: printerws,
        baseUrl: printerws.printer.connection.baseUrl
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
#home-page{
  min-height: 100%;
  display:flex;
  flex-direction:row;
  justify-content:flex-start;
  align-content:center;
} 
</style>

