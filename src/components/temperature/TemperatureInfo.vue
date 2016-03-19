<script>
  require('../../services/printer-service.js')
  export default {
    data () {
      return {
        isHeating: false,
        printerService: printerws
      }
    },
    props: {
      value: '',
      name: ''
    },
    methods: {
    }
  }
</script>

<template>
  <div class="temperature-info clear-fix" v-bind:class="{'is-open': isOpen}">
    <h3>{{name}}</h3>
    <span v-bind:class="{'is-heating': isHeating}">{{value}}C</span>
  </div>
</template>


<style>
  .label.is-moving {
    -webkit-animation: beat  5s linear infinite;
    -moz-animation: beat 5s linear infinite;
    -ms-animation: beat 5s linear infinite;
    animation: beat 5s linear infinite;
  }
  .temperature-info{
    text-align: center;
    margin-bottom:8px;
    height: 80px;
  }
  .temperature-info h3{
    color: #aaa;
    font-family: 'Exo', sans-serif;
    font-weight: 700;
    text-transform: uppercase;
    font-size:1em;
    margin-bottom:-8px;
  }
  .temperature-info span{
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
