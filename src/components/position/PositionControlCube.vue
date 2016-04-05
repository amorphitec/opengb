<script>
  require('../../services/printer-service.js')
  import SlideSwitch from '../../components/slideSwitch/SlideSwitch.vue'

  export default {
    components: {
      SlideSwitch
    },
    data () {
      return {
        isMoving: false,
        side: 'edge',
        resolution: 10,
        printerService: printerws
      }
    },
    props: {
    },
    computed: {
      motorStatus: function () {
        var test = this.printerService.printer.steppers.enabled
        console.log(this.printerService.printer.steppers)
        return  test ? 'on' : 'off'
      }
    },
    methods: {
      jogUpX: function () {
        var displacement = {x: this.resolution}
        this.printerService.setPositionRelative(displacement)
      },
      jogDownX: function () {
        var displacement = {x: -this.resolution}
        this.printerService.setPositionRelative(displacement)
      },
      jogUpY: function () {
        var displacement = {y: this.resolution}
        this.printerService.setPositionRelative(displacement)
      },
      jogDownY: function () {
        var displacement = {y: -this.resolution}
        this.printerService.setPositionRelative(displacement)
      },
      jogUpZ: function () {
        var displacement = {z: this.resolution}
        this.printerService.setPositionRelative(displacement)
      },
      jogDownZ: function () {
        var displacement = {z: -this.resolution}
        this.printerService.setPositionRelative(displacement)
      },
      setResolution: function (res) {
        this.resolution = res
      },
      homePrinter: function () {
        this.printerService.homePrintHead({x:true,y:true,z:true})
      },
      toggleMotors: function () {
        if(this.printerService.printer.steppers.enabled) {
          this.printerService.disengageMotors()
        } else {
          this.printerService.engageMotors()
        }
      }
    }
  }
</script>

<template>
  <div id="cube-wrapper">

    <div id="cube" class="edge-top">
      <div class="face one">
        <div flex="30" style="position:relative;width:30%;;height:100%;float:left;">
          <div id="x-down" class="ctrl" v-on:click="jogDownX()"></div>
        </div>
        <div layout="column" flex="40" layout-align="center center" style="position:relative;width:40%;;height:100%;float:left;">
          <div class="ctrl" style="width:90%" flex="50" id="y-down" v-on:click="jogDownY()"></div>
          <div class="ctrl" style="width:90%" flex="50" id="y-up" v-on:click="jogUpY()"></div>
        </div>
        <div flex="30" style="position:relative;width:30%;height:100%;float:left;">
          <div class="ctrl" id="x-up" v-on:click="jogUpX()"></div>
        </div>
      </div>
      <div class="face two">
        <div class="ctrl" id="z-down" v-on:click="jogDownZ()"></div>
        <div class="ctrl" id="z-up" v-on:click="jogUpZ()"></div>
      </div>
    </div>
    <div id="cube-resolution">
      <button class="button resolution-select" v-bind:class="{'selected': resolution == 0.1}" v-on:click="setResolution(0.1)">0.1mm</button>
      <button class="button resolution-select" v-bind:class="{'selected': resolution == 1}" v-on:click="setResolution(1)">1mm</button>
      <button class="button resolution-select" v-bind:class="{'selected': resolution == 10}" v-on:click="setResolution(10)">10mm</button>
      <button class="button resolution-select" v-bind:class="{'selected': resolution == 100}" v-on:click="setResolution(100)">100mm</button>
      <button class="button" style="width:100%;" v-on:click="homePrinter()" >Home All</button>
      <slide-switch v-on:click="toggleMotors()" v-bind:is-on="motorStatus == 'on'" label-text="motors"></slide-switch>
    </div>
  </div>
</template>


<style>

/*   BEGIN CUBE DEFINITION   */
#cube-resolution{
    min-height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-content: center;  
    width:100px;
}
.resolution-select{
   opacity:0.6;
   color:#444!important;
}
.resolution-select.selected{
   opacity:1;
}
#cube .ctrl:hover{background:rgba(200,200,200,.8);}
#x-down{width:80%;height:90%;position:absolute;top:5%;left:20%;border-radius:0 15px 15px 0;background: #000;}
#y-up{width:90%;height:40%;position:absolute;top:7%;left:5%;border-radius:0 0 15px 15px;background: #000;}
#y-down{width:90%;height:40%;position:absolute;bottom:7%;left:5%;border-radius:15px 15px 0 0;background: #000;}
#x-up{width:80%;height:90%;position:absolute;top:5%;right:20%;border-radius:15px 0 0 15px;background: #000;}
#z-up{width:90%;height:42%;position:absolute;top:5%;left:5%;border-radius:0 0 15px 15px;background: #000;}
#z-down{width:90%;height:42%;position:absolute;bottom:5%;left:5%;border-radius:15px 15px 0 0;background: #000;}
.position-status{transition:all 1s;}
#cube-wrapper{
  height:350px;
  margin-bottom:50px;
  position: relative;
}
#cube-info{height:50px;position:absolute;bottom:-50px;width:100%;}  
#cube, #cube .face {
  position: absolute;
  top: 55px ;
  left: 50%;
}
.face {
background:white;
  box-sizing: border-box;
  border: solid 1px;
  margin: -80px;
  width: 160px;
  height: 160px;
  transition: transform .7s;
  /** backface-visibility: hidden; /**/
}
/*   BEGIN CUBE ROTATIONS  */
#cube .one, #cube .two{ z-index:100;}
#cube.front .one  {
  -webkit-transform: perspective(600px)  rotateX(0deg) rotateY(0deg) rotateX(90deg) translateZ(80px);
  -ms-transform: perspective(600px) rotateX(0deg) rotateY(0deg) rotateX(90deg) translateZ(80px);
  transform: perspective(600px) rotateX(0deg) rotateY(0deg) rotateX(90deg) translateZ(80px);
  border: solid black 8px;
  border-radius:20px 20px 0 0;
  z-index:99;
}
#cube.front .two {
  -webkit-transform: perspective(600px) rotateX(0deg) rotateY(0deg) rotateX(0deg) translateZ(80px);
  -ms-transform: perspective(600px) rotateX(0deg) rotateY(0deg) rotateX(0deg) translateZ(80px);
  transform: perspective(600px) rotateX(0deg) rotateY(0deg) rotateX(0deg) translateZ(80px);
  border: solid black 8px;
  border-radius:0 0 20px 20px;
}
#cube.edge-top .one  {

  -webkit-transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(90deg) translateZ(80px);
  -ms-transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(90deg) translateZ(80px);
  transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(90deg) translateZ(80px);
  border: solid black 8px;
  border-radius:20px 20px 0 0;
  border-bottom: 0;
}
#cube.edge-top .two {
  -webkit-transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(0deg) translateZ(80px);
  -ms-transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(0deg) translateZ(80px);
  transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(0deg) translateZ(80px);
  border: solid black 8px;
  border-radius:0 0 20px 20px;
  border-top: 0;
  z-index:99;
}
#cube.edge-front .one  {
  -webkit-transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(90deg) translateZ(80px);
  -ms-transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(90deg) translateZ(80px);
  transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(90deg) translateZ(80px);
  border: solid black 8px;
  border-radius:20px 20px 0 0;
  border-bottom: 0;
  z-index:99;
}
#cube.edge-front .two {
  -webkit-transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(0deg) translateZ(80px);
  -ms-transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(0deg) translateZ(80px);
  transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(0deg) translateZ(80px);
  border: solid black 8px;
  border-radius:0 0 20px 20px;
  border-top: 0;
}
#cube.top .one  {
  -webkit-transform: perspective(600px) rotateX(-90deg) rotateY(0deg) rotateX(90deg) translateZ(80px);
  -ms-transform: perspective(600px) rotateX(-90deg) rotateY(0deg) rotateX(90deg) translateZ(80px);
  transform: perspective(600px) rotateX(-90deg) rotateY(0deg) rotateX(90deg) translateZ(80px);
  border: solid black 8px;
  border-radius:20px 20px;
}
#cube.top .two {
  -webkit-transform: perspective(600px) rotateX(-90deg) rotateY(0deg) rotateX(0deg) translateZ(80px);
  -ms-transform: perspective(600px) rotateX(-90deg) rotateY(0deg) rotateX(0deg) translateZ(80px);
  transform: perspective(600px) rotateX(-90deg) rotateY(0deg) rotateX(0deg) translateZ(80px);
  border: solid black 8px;
  border-radius:20px;
  z-index:99;
}
/*   END CUBE ROTATIONS  */
/*   END CUBE DEFINITION  */
</style>
