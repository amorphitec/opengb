<template>
  
  <div class="off-canvas position-left reveal-for-large" id="side-nav" data-off-canvas data-position="left">
    <div class="row column">
      <ul class="property-nav">
        <li class="library">
          <a ui-sref="library" href="/library">
            {{show}}
            <i class="fi-home"></i>HOME
          </a>
        </li>
      </ul>
    </div>
  </div>

</template>

<script>
export default {
  data () {
    return {
      pages: {
        home:{name:'my openGB',url:'home',icon:'home'},
        controls:{name:'controls',url:'controls',icon:'open_with'},
        files:{name:'my files',url:'files',icon:'folder'},
        statistics:{name:'statistics',url:'statistics',icon:'equalizer'},
        settings:{name:'settings',url:'settings',icon:'settings'}        
      }
    }
  }
}
</script>

<style>
  .left-sidebar {
      box-shadow: 1px 0px 2px rgba(0,0,0,0.1);
      font-family: 'proxima_nova_condensedSBd';
      background-color: white;
      padding: 0;
      z-index: 3000;
      width: 45px;
      min-height: 100%;
      overflow: hidden;
      display: inline;
      -webkit-transition: width 0.5s;
      transition: width 0.5s;
      -webkit-transition-timing-function: ease;
      transition-timing-function: ease;
  }
</style>
