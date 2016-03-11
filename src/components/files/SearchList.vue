<script>
  require('../../services/printer-service.js')
  var _ = require('lodash')
  export default {
    data () {
      return {
        files: [],
        uploadFile: [],
        selectedFile: printerws.selectedFile,
        searchString: '',
        filteredFiles: [],
        view: 'default',
        page: 1,
        loading: []
      }
    },
    computed: {
      filesPage: function () {
        var fileList = []
        for( var i = 0 ; i < 5 ; i++ ) {
          var j = (this.page - 1) * 5 + i
          if(this.filteredFiles[j]){
            fileList.push(this.filteredFiles[j])
          }
        }
        return fileList
      }
    },
    methods: {
      selectFile: function (fid, e) {
        this.loading.length = 0
        this.loading.push(fid)
        printerws.getFile(fid)
      },
      filterFiles: function () {
        if (this.searchString.length > 0) {
          var regex = new RegExp(this.searchString, 'i')
          var result = _.filter(this.files, function (elem) {
            var elemTestString = elem.name + ' ' + elem.url + ' ' + _(elem.tags).toString()
            return regex.test(elemTestString)
          })
          this.filteredFiles = result
        } else {
          this.filteredFiles = this.files
        }
      },
      nextPage: function () {
        this.page = this.page + 1;
      },
      prevPage: function () {
        this.page = this.page - 1;
      }
    },
    ready: function () {
      var vm = this
      setTimeout(function () {
        printerws.getFiles()
        setTimeout(function () {
          vm.$nextTick(function () {
            vm.files = printerws.files
            vm.filterFiles()
          })
        }, 500)
      }, 500)
    }
  }

</script>

<template>
  
  <div class="search-list">
    <input class="search-input" placeholder="search your files" v-model="searchString" v-on:keyup="filterFiles">
    <div id="file-list">
      <div id="fli-{{file.id}}" 
           v-for="file in filesPage" 
           class="file-list-item clear-fix"
           v-on:click="selectFile(file.id, $event)">
        <span class="badge" v-bind:class="{'pulse1': file.id == loading[0]}" >
          {{file.name.substr(0,1).toUpperCase() + file.name.substr(1,1).toLowerCase()}}
        </span>
        <span class="file-info file-name">{{file.name}}</span>
        <span class="file-info center small">{{(file.size/1000).toFixed(2)}}kB</span>
        <span class="file-info center small">3/11/16</span>
      </div>
    </div>
    <div>
      <button class="button" v-if="page > 1" v-on:click="prevPage()">&lt; prev</button>
      <button class="button" v-if="page < (filteredFiles.length / 5)" v-on:click="nextPage()" style="float:right">next &gt;</button>
    </div>
  </div>

</template>


<style>
  .small{
    font-size: .7em;
  }
  .padded{
    padding: 5px;
  }
  .search-list{margin: 0 20px;}
  .search-input{
    width: 100%;
    font-size: 1.5em;
    padding: 10px 10px;
    padding-bottom: 0px;
    padding-left: 0;
    color: #333;
    border: 0;
    border-bottom: 5px #ddd solid;
    display:none;
  }
  .search-input:focus{outline: none;}
  #file-list{
    min-height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-content: center;
    flex-wrap: wrap;
  }
  .file-list-item{
    background: #ccc;
    padding:5px;
    margin-bottom:5px;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    overflow: hidden;
  }
  .file-list-item:hover{
    color:#444;
  }
  .file-list-item .badge{
    line-height: 24px;
    border:5px solid white;
    background: transparent;
    font-size: 1.2em;
    height: 45px;
    width: 45px;
    color:#444;
  }

  .file-info{
    width:130px;
    margin-left: 20px;
    word-wrap: break-word;
    white-space: pre;
  }
  .file-info.center{
    text-align: center;
  }

  .pulse1 {
    -webkit-animation: pulse1 1.5s linear 4;
    -moz-animation: pulse1 1.5s linear 4;
    -ms-animation: pulse1 1.5s linear 4;
    animation: pulse1 1.5s linear 4;
  }

  @keyframes pulse1 {
   0% {
      color: rgba(25, 25, 25, 1)
   }
   90% {
      color: rgba(255, 255, 255, 0.0)
   }
   100% {
      color: rgba(255, 255, 255, 1.0)
   }

  }

  @-moz-keyframes pulse1 {
   0% {
      color: rgba(25, 25, 25, 1)
   }
   90% {
      color: rgba(255, 255, 255, 0.0)
   }
   100% {
      color: rgba(255, 255, 255, 1.0)
   }

  }

  @-webkit-keyframes pulse1 {
   0% {
      color: rgba(25, 25, 25, 1)
   }
   90% {
      color: rgba(255, 255, 255, 0.0)
   }
   100% {
      color: rgba(255, 255, 255, 1.0)
   }

  }

  @-ms-keyframes pulse1 {
   0% {
      color: rgba(25, 25, 25, 1)
   }
   90% {
      color: rgba(255, 255, 255, 0.0)
   }
   100% {
      color: rgba(255, 255, 255, 1.0)
   }

}
</style>
