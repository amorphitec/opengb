<script>
  // libs and services
  require('../services/printer-service.js')
  import PrintStatusCircle from '../components/print/PrintStatusCircle.vue'
  import TemperatureMenu from '../components/temperature/TemperatureMenu.vue'
  import SearchList from '../components/files/SearchList.vue'

  export default {
    components: {
      PrintStatusCircle,
      TemperatureMenu,
      SearchList
    },
    data () {
      return {
        printerService: printerws,
        files: {},
        selectedFile: printerws.selectedFile,
        uploadFile:{},
        view: 'file-selection',
        fileInfoWidth: ''
      }
    },
    ready: function () {
      console.log('childNodes: ', this.$el.childNodes)
    },
    computed: {
      isFileSelection: function () {
        console.log(this.view)
        return this.view === 'file-selection'
      },
      isFileInfo: function () {
        return this.view === 'file-info'
      },
      showFileInfo: function () {
        var isPrinting = this.printerService.printer.state != 'READY' && this.printerService.printer.state != 'ERROR'
        var hasFile = this.printerService.selectedFile.length > 0
        console.log('tests',[isPrinting, hasFile, this.printerService.selectedFile])
        return isPrinting || hasFile
      },
      statusState: function () {
        var s = this.printerService.printer.state
        if (s == 'EXECUTING') {
          s = 'Heating/Printing'
        }
        return s
      },
      isNotPrinting: function () {
        var s = this.printerService.printer.state
        return s != 'EXECUTING' && s != 'PAUSED'
      }
    },
    methods: {
      setView: function (v) {
        this.view = v
        var vm = this
        setTimeout(
          function () {
            vm.$set('fileInfoWidth', vm.$el.childNodes[5].clientWidth)
          },
          2000
        )
      },
      homePrinter: function () {
        this.printerService.homePrintHead({x:true,y:true,z:true})
      },
      deselectFile: function () {
        printerws.deselectFile()
      },
      printFile: function () {
        if (this.selectedFile[0] && this.selectedFile[0].content) {
          printerws.printFile(this.selectedFile[0].id)
        }
      },
      pausePrint: function () {
        printerws.pausePrint()
      },
      resumePrint: function () {
        printerws.resumePrint()
      },
      cancelPrint: function () {
        printerws.cancelPrint()
      },
      initFileSelect: function () {
        document.getElementById('uploadFile').click();
      },
      onFileChange: function (e) {
        console.log('file changed',e)
        var files = e.target.files || e.dataTransfer.files
        if (files.length) {
          var file;
          var vm = this

          var fr = new FileReader();
          fr.onload = function(e){
            var contents = e.target.result;
            file = {
              'name': files[0].name,
              'contents': contents,
              'image': null,
              'meta': {}
            }
            vm.saveFile(file);
          }
          fr.readAsText(files[0]);
        } else {
          return;
        }
      },
      saveFile: function (file) {
        printerws.putFile(file)
      },
      deleteFile: function (fid) {
        printerws.deleteFile(fid)
      }
    },
    watch: {
      'selectedFile': {
        handler: function (newVal, oldVal) {
          if (newVal[0] && newVal[0].id) {
            this.setView('file-info')
          }
        }
      }
    }

  }
</script>

<template>
  <section id="home-page">

    <div id="temperature-wrapper">
      <temperature-menu 
        friendly-name="Heated Bed"
        temp-id="bed"
        v-bind:current="printerService.printer.temperatures.bed.current"
        v-bind:target="printerService.printer.temperatures.bed.target"
        >
      </temperature-menu>
      <temperature-menu 
        friendly-name="Extruder 1"
        temp-id="nozzle1"
        v-bind:current="printerService.printer.temperatures.nozzle1.current"
        v-bind:target="printerService.printer.temperatures.nozzle1.target"
        >
      </temperature-menu>
      <temperature-menu 
        friendly-name="Extruder 2"
        temp-id="nozzle2"
        v-bind:current="printerService.printer.temperatures.nozzle2.current"
        v-bind:target="printerService.printer.temperatures.nozzle2.target"
        >
      </temperature-menu>
      <button class="button" v-on:click="homePrinter()" v-if="isNotPrinting">Home All</button>
    </div>

    <div id="file-selection" v-bind:class="{'is-focus': isFileSelection}" v-if="isNotPrinting" v-on:click="setView('file-selection')">

      <button id="file-upload" class="button" type="button" v-on:click="initFileSelect">
        Upload a File
      </button>
      <input 
        id="uploadFile" 
        class="hide"
        type="file"
        accept=".gcode"
        v-on:change="onFileChange"/>

      <search-list></search-list>
    </div>

    <div id="file-info" v-if="showFileInfo" v-bind:class="{'is-focus': isFileInfo}" v-on:click="setView('file-info')">

      <span id="file-image" v-bind:class="{hide: selectedFile[0]===null}">
        
        <h2>{{printerService.selectedFile[0]!=null ? printerService.selectedFile[0].name : ''}}</h2>

        <print-status-circle 
          v-bind:state="statusState"
          v-bind:size="300" 
          v-bind:value="printerService.printer.print.currentLine" 
          v-bind:goal="printerService.printer.print.totalLines">
        </print-status-circle>

        <button 
          type="button" 
          v-on:click="printFile()" 
          v-bind:class="{hide: printerService.printer.state != 'READY'}" 
          class="button">
          Print
        </button>

        <button 
          type="button" 
          v-on:click="pausePrint()"  
          v-bind:class="{hide: (printerService.printer.state != 'EXECUTING')}" 
          class="button">
          Pause
        </button>
        
        <button type="button" 
          v-on:click="resumePrint()" 
          v-bind:class="{hide: (printerService.printer.state != 'PAUSED')}" 
          class="button">
          Resume
        </button>
        
        <button 
          type="button" 
          v-on:click="cancelPrint()" 
          v-bind:class="{hide: (printerService.printer.state != 'EXECUTING') }" 
          class="button">
          Stop
        </button>

        <div>{{printerService.printer.state}}</div>
 
      </span>

      <div>
        details
      </div>

      <button 
        type="button" 
        v-on:click="deleteFile()" 
        class="button alert">
        Delete File
      </button>

    </div>

  </section>
</template>

<style>

h2{
  text-align: center;
  font-family: 'proxima_novalight';
}

#home-page{
  min-height: 100%;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-content: center;
} 
#temperature-wrapper{
  flex: 0;
}
#file-upload{
  margin: 0px 20px;
}
#file-selection{
  flex: 1;
  min-width: 250px;
  transition: all .5s;
}
#file-selection.is-focus{
  flex: 8;
  min-width: 70%;
}
#file-info{
  text-align: center;
  flex: 1;
  transition: all .5s;
}
#file-info.is-focus{
  flex: 8;
}
#file-image{
  margin: 20px auto;
}
#file-info.is-focus #file-image i{
  font-size: 3em;
  margin-bottom: 0;
  line-height: 0;
  color: black;
  position: relative;
  bottom: 30px;
}
#file-image.hide{
  width: 0;
  padding-top: 0;
}
#file-image i{
  font-size: 0px;
}
.drop-box {
  background: #F8F8F8;
  border: 5px dashed #DDD;
  width: 60%;
  height: 65px;
  text-align: center;
  padding-top: 25px;
  margin: 0px auto;
}
.drop-box.drag-over{
  background: #eee;
  border-color: #cfc;
} 
#files-page{
  position: relative;
  min-height: 100%;
}
#renderArea {
  position: relative;
  left: 0;
  top: 0;
  width: 100%;
  height: calc(100vh - 100px);
  z-index: 0;
}

#renderArea md-progress-circular {
  position: absolute;
  z-index: -1;
  left: 50%;
  top: 50%;
  margin-left: -50px;
  margin-top: -50px;
}

#left-column{
  float: left;
}

#right-column{
  float: left;
}

</style>

