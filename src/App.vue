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
  </div>
</template>

<script>
  import wsinst from './services/websocket-service.js'

  export default {
    components: {
    },
    methods: {
      toggleSideNav: function () {
        this.showSideNav = !this.showSideNav
      }
    },
    data () {
      return {
        showSideNav: false,
        pages: {
          home: {name: 'my openGB', url: 'home', icon: 'fi-home'},
          controls: {name: 'controls', url: 'controls', icon: 'fi-layout'},
          files: {name: 'my files', url: 'files', icon: 'fi-page'},
          statistics: {name: 'statistics', url: 'statistics', icon: 'fi-graph-bar'},
          settings: {name: 'settings', url: 'settings', icon: 'fi-widget'}
        }
      }
    }
  }
</script>

<style>
  .off-canvas-content .off-canvas-content{
    box-shadow: none;
  }
  #main-container{min-height: 100vh;}
  #side-nav{
    min-height: 100vh;
    z-index: 100;
    transition: width .5s;
  }
  #side-nav:hover{width: 165px!important;}
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
  .callout{height: 100vh!important;margin: 0!important;border: 0!important;}
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
