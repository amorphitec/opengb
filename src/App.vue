<template>
  <div id="main-container" class="off-canvas-wrapper">
    <div class="off-canvas-wrapper-inner"  v-bind:class="{'is-partially-open-left': showSideNav}" data-off-canvas-wrapper>
      <div class="off-canvas position-left reveal-for-medium small" id="side-nav" v-bind:class="{'is-open': showSideNav}" data-off-canvas data-position="left">
          <div class="left-sidebar">
            <ul class="property-nav">
              <li class="row column" v-for="page in pages">
                <a class="item" v-link="page.url">
                   <i class="{{page.icon}}"></i>
                </a>
              </li>
            </ul>
            <ul class="property-nav bottom">
              <li class="row column">
                <a class="item" v-on:click="toggleEmStop()">
                  <i class="fi-prohibited"></i>
                </a>
              </li>
            </ul>
        </div>
      </div>
      <div id="full-col" class="off-canvas-content" v-bind:class="{'is-open': showSideNav}" data-off-canvas-content>
        <div class="title-bar hide-for-medium">
          <div class="title-bar-left">
            <button class="menu-icon" type="button" data-open="side-nav" v-on:click="toggleSideNav"></button>
            <span class="title-bar-title">OpenGigabot</span>
          </div>
        </div>
        <div class="callout">
          <router-view></router-view>
        </div>
      </div>
    </div>
    
    <div id="full-screen" v-if="emStop">
      <div class="huge-button" v-on:click="emergencyStop()">Emergency Stop</div>
    </div>
    
    <div id="full-screen" v-if="filamentSwap">
      <filament-swap></filament-swap>
    </div>
    
    <div id="error" v-if="hasNoWsConnection">
      Error, websocket connection is disconnected go to <a v-link="'settings'">Settings</a> to fix or check raspberry pi
    </div>
    
    <div id="error" v-if="hasNoPrinterConnection">
      Error, printer is not connected to raspberry pi, please connect and <span v-on:click="reloadPage()"><a>reload the page</a></span> 
    </div>
    
    <div id="error" v-if="hasPrinterError">
      Error, please restart opengb on raspberry pi
    </div>

  </div>
</template>

<script>

  import FilamentSwap from './pages/modals/FilamentSwap.vue'
  require('./services/printer-service.js')

  export default {
    components: {
      FilamentSwap
    },
    methods: {
      toggleSideNav: function () {
        this.showSideNav = !this.showSideNav
      },
      toggleEmStop: function () {
        this.emStop = !this.emStop
      },
      emergencyStop: function () {
        this.printerService.emergencyStop()
      },
      reloadPage: function () {
        location.reload(true);
      }
    },
    computed:{
      hasNoWsConnection: function () {
        return this.printerService.printer.state === null
      },
      hasNoPrinterConnection: function () {
        return this.printerService.printer.state === 'DISCONNECTED'
      },
      hasPrinterError: function () {
        return this.printerService.printer.state === 'ERROR'
      },
      filamentSwap: function () {
        return this.printerService.printer.state === 'FILAMENT_SWAP'
      }
    },
    data () {
      return {
        printerService : printerws,
        showSideNav: false,
        emStop: false,
        pages: {
          home: {name: 'my openGB', url: 'home', icon: 'fi-home'},
          controls: {name: 'controls', url: 'controls', icon: 'fi-layout'},
          // files: {name: 'my files', url: 'files', icon: 'fi-page'},
          // statistics: {name: 'statistics', url: 'statistics', icon: 'fi-graph-bar'},
          settings: {name: 'settings', url: 'settings', icon: 'fi-widget'}
        }
      }
    }
  }
</script>

<style>
  body{
    font-family: 'Roboto', sans-serif;
  }
  .button{
    font-family: 'Exo', sans-serif;
    font-weight: 700;
    text-transform: uppercase;  
  }
  .off-canvas-content .off-canvas-content{
    box-shadow: none;
  }
  #main-container{
    min-height: 100vh;
  }
  #side-nav{
    min-height: 100vh;
    z-index: 100;
    transition: width .5s;
  }
  /*#side-nav:hover{width: 165px!important;}*/
  #side-nav.small{width: 50px;overflow: hidden;background: rgba(0,0,0,.9);}
  #full-col{
    box-shadow: none;
    background: #fff;
  }
  .property-nav li {
      width: 175px;
      list-style-type: none;
      font-size: 40px;
      border-bottom: thin solid none;
      margin-left: -20px;
      padding: 0;
      text-align: center;
      width: 50px;
  }
  .property-nav li a{
    color: #aaa;
  }
  .property-nav.bottom{
    position:absolute;
    bottom:0;
  }
  .callout{height: 100vh!important;margin: 0!important;border: 0!important;}
  #error{
    width: 100%;
    height: 50px;
    color:white;
    text-align: center;
    line-height: 40px;
    position: fixed;
    bottom:0;
    background:#c60f13;
  }

  .off-canvas.position-left {
    left: -50px!important;
    top: 0;
    width: 50px!important;
  }
  .is-partially-open-left {
    -webkit-transform: translateX(50px)!important;
    -ms-transform: translateX(50px)!important;
    transform: translateX(50px)!important;
  }
  
  #full-screen{
    position:fixed;
    background: rgba(0,0,0,.9);
    top:0;
    left:0;
    width:100vw;
    height: 100vh;
  }

  .huge-button{
    margin:10%;
    text-align: center;
    background:#ccc;
    line-height: 50vh;
    font-size: 2em;
    cursor: pointer;
  }
  .huge-button:hover{
    background:#aaa;
  }

  @media screen and (min-width: 40em){
   .position-left.reveal-for-medium ~ .off-canvas-content {
      margin-left: 50px!important; 
    }  
   .position-left.reveal-for-medium ~ .off-canvas-content.is-open {
      margin-left: 0px!important; 
    }  
    .off-canvas.position-left {
      left: 0px!important;
    }
    .off-canvas.position-left.is-open {
      left: -50px!important;
    }
  }
</style>
