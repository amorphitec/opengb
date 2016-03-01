<script>
require('d3')

export default {
  data () {
    return {
    }
  },
  props: {
    state: '',
    size: '',
    goal: '',
    value: ''
  },
  methods: {
    calculateGoalPath: function () {
      return this.calculatePath(1, 1)
    },
    calculateValuePath: function () {
      if (this.value && this.goal) {
        return this.calculatePath(this.value, this.goal)
      } else {
        return this.calculatePath(0, 1)
      }
    },
    calculatePath: function (val, goal) {
      var angle = (!!val && !!goal) ? val / goal * 2 * Math.PI : 0
      var path = d3.svg.arc()
                .innerRadius(this.size / 2 - 20)
                .outerRadius(this.size / 2)
                .startAngle(0)
                .endAngle(angle)
      return path()
    }
  },
  computed: {
    percentComplete: function () {
      var percent = 0
      if (this.value && this.goal) {
        percent = (this.value / this.goal * 100).toFixed(0)
      }
      return percent
    },
    path: function () {
    },
    transform: function () {
      var trans = 'translate(' + this.size / 2 + ',' + this.size / 2 + ')'
      return trans
    }
  }
}
</script>

<template>
  <div>  
    <svg v-bind:width="size" v-bind:height="size" >
      <circle v-bind:r="size/2" v-bind:transform="transform" v-bind:class="{'pulse': state == 'EXECUTING'}">
      </circle>
      <path v-bind:d="calculateGoalPath()" fill="#ccc" v-bind:transform="transform">
      </path>
      <path v-bind:d="calculateValuePath()" fill="#fecc09" v-bind:transform="transform">
      </path>
      <text style="font-size: 50px;" alignment-baseline="middle" text-anchor="middle"  v-bind:transform="transform" >{{percentComplete}}%</text> 
    </svg>
  </div>
</template>


<style>
  #svg-holder{
    overflow: hidden;
  }
  svg, path{
    transform: all 1s;
  }
  circle{
    fill: #000;
    opacity: 0;
  }

  circle.pulse {
    -webkit-animation: pulse  5s linear infinite;
    -moz-animation: pulse 5s linear infinite;
    -ms-animation: pulse 5s linear infinite;
    animation: pulse 5s linear infinite;
  }
  
  @keyframes pulse {
    0% {
      opacity: 0;
    }
    50% {
      opacity: 0.2;
    }
    100% {
      opacity: 0;
    }
  }

  @-moz-keyframes pulse {
    0% {
      opacity: 0;
    }
    50% {
      opacity: 0.2;
    }
    100% {
      opacity: 0;
    }
  }

  @-webkit-keyframes pulse {
    0% {
      opacity: 0;
    }
    50% {
      opacity: 0.2;
    }
    100% {
      opacity: 0;
    }
  }

  @-ms-keyframes pulse {
    0% {
      opacity: 0;
    }
    50% {
      opacity: 0.2;
    }
    100% {
      opacity: 0;
    }
  }

</style>
