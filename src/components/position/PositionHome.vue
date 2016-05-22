<script>
  require('../../services/printer-service.js')
  export default {
    data () {
      return {
        isMoving: false,
        printerService: printerws
      }
    },
    props: {
      name: ''
    },
    methods: {
      toggleOpen: function () {
        this.isOpen = !this.isOpen
      }
    }
  }
</script>

<template>
  <div class="position-home">
    <div class="clear-fix button">
      home {{name}}
    </div>
  </div>
</template>


<style>
  .position-home{
    text-align: center;
    margin-bottom:30px;
  }
</style>
