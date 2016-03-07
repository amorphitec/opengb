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

    <input class="search-input" placeholder="address for printer" v-model="baseUrl" v-on:blur="setBaseUrl">

  </section>
</template>

<style>

h2{
  text-align: center;
  font-family:'proxima_novalight';
}

#home-page{
  min-height: 100%;
  display:flex;
  flex-direction:row;
  justify-content:flex-start;
  align-content:center;
} 
</style>

