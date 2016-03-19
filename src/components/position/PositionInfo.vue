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
      value: '',
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
  <div class="position-info clear-fix" v-bind:class="{'is-open': isOpen}">
    <h3>{{name}}</h3>
    <span v-bind:class="{'is-moving': isMoving}">{{((value * 100) / 100).toFixed(2)}}</span>
  </div>
</template>


<style>
  .label.is-moving {
    -webkit-animation: beat  5s linear infinite;
    -moz-animation: beat 5s linear infinite;
    -ms-animation: beat 5s linear infinite;
    animation: beat 5s linear infinite;
  }
  .position-info{
    text-align: center;
    margin-bottom: 15px;
  }
  .position-info h3{
    color: #aaa;
    font-family: 'Exo', sans-serif;
    font-weight: 700;
    text-transform: uppercase;
    font-size:1em;
    margin-bottom:-8px;
  }
  .position-info span{
    font-family: 'Exo', sans-serif;
    font-weight: 200;
    text-transform: uppercase;
    font-size:2.2em;
  }
  @keyframes beat {
    0% {
      opacity: 0.7;
    }
    50% {
      opacity: 1;
    }
    100% {
      opacity: 0.7;
    }
  }

  @-moz-keyframes beat {
    0% {
      opacity: 0.7;
    }
    50% {
      opacity: 1;
    }
    100% {
      opacity: 0.7;
    }
  }

  @-webkit-keyframes beat {
    0% {
      opacity: 0.7;
    }
    50% {
      opacity: 1;
    }
    100% {
      opacity: 0.7;
    }
  }

  @-ms-keyframes beat {
    0% {
      opacity: 0.7;
    }
    50% {
      opacity: 1;
    }
    100% {
      opacity: 0.7;
    }
  }

</style>
