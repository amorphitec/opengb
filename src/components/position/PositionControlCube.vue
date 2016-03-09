<script>
  require('../../services/printer-service.js')
  export default {
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
      }
    }
  }
</script>

<template>
  <div id="cube-wrapper">
    <div id="cube" class="edge-top">
      <div class="face one">
        <div class="ctrl" id="x-down" v-on:click="jogDownX()"></div>
        <div class="ctrl" id="y-up" v-on:click="jogUpY()"></div>
        <div class="ctrl" id="y-down" v-on:click="jogDownY()"></div>
        <div class="ctrl" id="x-up" v-on:click="jogUpX()"></div>
      </div>
      <div class="face two">
        <div class="ctrl" id="z-up" v-on:click="jogUpZ()"></div>
        <div class="ctrl" id="z-down" v-on:click="jogDownZ()"></div>
      </div>
    </div>
    <div id="cube-resolution">
      <button class="button">0.1mm</button>
      <button class="button">1mm</button>
      <button class="button">10mm</button>
      <button class="button">100mm</button>
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
#cube{position:relative;top:175px;left:100px;}
#cube .ctrl:hover{background:rgba(200,200,200,.8);}
#x-down{width:50px;height:218px;border:solid black 2px;position:absolute;top:10px;left:10px;border-radius:5px;}
#y-up{width:100px;height:103px;border:solid black 2px;position:absolute;margin-left:-50px;top:10px;left:50%;border-radius:5px;}
#y-down{width:100px;height:103px;border:solid black 2px;position:absolute;margin-left:-50px;bottom:10px;left:50%;border-radius:5px;}
#x-up{width:50px;height:218px;border:solid black 2px;position:absolute;top:10px;right:10px;border-radius:5px;}
#z-up{width:200px;height:103px;border:solid black 2px;position:absolute;margin-left:-100px;top:10px;left:50%;border-radius:5px;}
#z-down{width:200px;height:103px;border:solid black 2px;position:absolute;margin-left:-100px;bottom:10px;left:50%;border-radius:5px;}
.position-status{transition:all 1s;}
#cube-wrapper{
  height:450px;
  width:400px;
}
#cube-info{height:50px;position:absolute;bottom:-50px;width:100%;}  
#cube .face {
  position: absolute;
  top: 50%;
  left: 50%;
}
.face {
background:white;
  box-sizing: border-box;
  border: solid 1px;
  margin: -120px;
  width: 240px;
  height: 240px;
  transition: transform .7s;
  /** backface-visibility: hidden; /**/
}
/*   BEGIN CUBE ROTATIONS  */
#cube .one, #cube .two{ z-index:100;}
#cube.front .one  {
  -webkit-transform: perspective(600px)  rotateX(0deg) rotateY(0deg) rotateX(90deg) translateZ(120px);
  -ms-transform: perspective(600px) rotateX(0deg) rotateY(0deg) rotateX(90deg) translateZ(120px);
  transform: perspective(600px) rotateX(0deg) rotateY(0deg) rotateX(90deg) translateZ(120px);
  border: solid black 2px;
  z-index:99;
}
#cube.front .two {
  -webkit-transform: perspective(600px) rotateX(0deg) rotateY(0deg) rotateX(0deg) translateZ(120px);
  -ms-transform: perspective(600px) rotateX(0deg) rotateY(0deg) rotateX(0deg) translateZ(120px);
  transform: perspective(600px) rotateX(0deg) rotateY(0deg) rotateX(0deg) translateZ(120px);
  border: solid black 2px;
}
#cube.edge-top .one  {

  -webkit-transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(90deg) translateZ(120px);
  -ms-transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(90deg) translateZ(120px);
  transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(90deg) translateZ(120px);
  border: solid black 2px;
  border-bottom: 0;
}
#cube.edge-top .two {
  -webkit-transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(0deg) translateZ(120px);
  -ms-transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(0deg) translateZ(120px);
  transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(0deg) translateZ(120px);
  border: solid black 2px;
  border-top: 0;
  z-index:99;
}
#cube.edge-front .one  {
  -webkit-transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(90deg) translateZ(120px);
  -ms-transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(90deg) translateZ(120px);
  transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(90deg) translateZ(120px);
  border: solid black 2px;
  border-bottom: 0;
  z-index:99;
}
#cube.edge-front .two {
  -webkit-transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(0deg) translateZ(120px);
  -ms-transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(0deg) translateZ(120px);
  transform: perspective(600px) rotateX(-45deg) rotateY(0deg) rotateX(0deg) translateZ(120px);
  border: solid black 2px;
  border-top: 0;
}
#cube.top .one  {
  -webkit-transform: perspective(600px) rotateX(-90deg) rotateY(0deg) rotateX(90deg) translateZ(120px);
  -ms-transform: perspective(600px) rotateX(-90deg) rotateY(0deg) rotateX(90deg) translateZ(120px);
  transform: perspective(600px) rotateX(-90deg) rotateY(0deg) rotateX(90deg) translateZ(120px);
  border: solid black 2px;
}
#cube.top .two {
  -webkit-transform: perspective(600px) rotateX(-90deg) rotateY(0deg) rotateX(0deg) translateZ(120px);
  -ms-transform: perspective(600px) rotateX(-90deg) rotateY(0deg) rotateX(0deg) translateZ(120px);
  transform: perspective(600px) rotateX(-90deg) rotateY(0deg) rotateX(0deg) translateZ(120px);
  border: solid black 2px;
  z-index:99;
}
/*   END CUBE ROTATIONS  */
/*   END CUBE DEFINITION  */

</style>
