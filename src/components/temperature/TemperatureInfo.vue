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
  <div class="position-info clear-fix" v-bind:class="{'is-open': isOpen}">
    <span>{{name}}</span>
    <span v-bind:class="{'is-heating': isHeating}">{{value}}</span>
  </div>
</template>


<style>
  .label.is-moving {
    -webkit-animation: beat  5s linear infinite;
    -moz-animation: beat 5s linear infinite;
    -ms-animation: beat 5s linear infinite;
    animation: beat 5s linear infinite;
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
