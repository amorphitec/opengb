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
        loading: []
      }
    },
    calulated: {
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
           v-for="file in filteredFiles" 
           class="file-list-item clear-fix"
           v-on:click="selectFile(file.id, $event)">
        <span class="badge float-left" v-bind:class="{'pulse1': file.id == loading[0]}" >
          {{file.name.substr(0,1).toUpperCase() + file.name.substr(1,1).toLowerCase()}}
        </span>
        <span class="float-left padded">
          <div>{{file.name}}</div>
          <div class="small">{{(file.size/1000).toFixed(2)}}kB</div>
        </span>
      </div>
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
  .search-list{margin: 0 20px;margin-bottom: 50px;}
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
    flex-direction: row;
    justify-content: flex-start;
    align-content: center;
    flex-wrap: wrap;
  }
  .file-list-item{
    /*background:#eee;*/
    cursor: pointer;
    width: 100%;
    margin: 5px 0;
    margin-right: 10px;
    border-radius: 25px 0 0 25px;

  }
  .file-list-item:hover{
    background:#fecc09;
    color:white;
  }
  .file-list-item .badge{
    border:5px solid #fecc09;
    background: white;
    font-size: 1.5em;
    height: 55px;
    width: 55px;
    color:#ccc;
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
