<script>
  require('../../services/printer-service.js')
  export default {
    props: ['isOn','labelText']
  }
</script>

<template>
  
  <div class="slide-switch button" v-bind:class="{'is-on':isOn}">
    <div class="slide-switch-off">Off</div>
    <div class="slide-switch-on">On</div>
    <div class="slide-switch-state">{{labelText}}</div>
  </div>

</template>


<style>
.slide-switch{
  margin:0 auto;
  width:150px;
  height:35px;
  position:relative;
}
.slide-switch div{
  transition: all 0.5s;
}
.slide-switch-on{
  width:30%;
  height:100%;
  position:absolute;
  top:0;
  right:0;
  background:green;
  padding:10px;
}
.slide-switch-off{
  width:30%;
  height:100%;
  position:absolute;
  top:0;
  left:0;
  background:red;
  padding:10px;
}
.slide-switch-state{
  width:70%;
  height:100%;
  position:absolute;
  top:0;
  right:0;
  background:white;
  padding:10px;
  color:#aaa;
}
.slide-switch.is-on .slide-switch-state{
  right:30%;
}
</style>
