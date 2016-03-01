(function (exports) {
  require('./websocket-service.js')
  'use strict'
  var ws
  var printer = {
    connection: { baseUrl: null, connected: false, printReady: false },
    position: { x: null, y: null, z: null },
    print: { currentLine: null, totalLines: null },
    state: null,
    temperatures: {
      bed: { target: null, current: null },
      nozzle1: { target: null, current: null },
      nozzle2: { target: null, current: null }
    },
    statistics: {
      temperatures: {
        bed: { target: [], current: [] },
        nozzle1: { target: [], current: [] },
        nozzle2: { target: [], current: [] }
      }
    }
  }
  var files = []
  var counters = []
  var selectedFile = []

  printer.connection.baseUrl = printer.connection.baseUrl || 'ws://' + location.hostname + ':' + location.port + '/ws'

  exports.printerws = {
    printer: printer,
    files: files,
    counters: counters,
    selectedFile: selectedFile,
    setTemperatures: function (temps) {
      var method = 'set_temp'
      var params = {
        'bed': temps.bed,
        'nozzle1': temps.nozzle1,
        'nozzle2': temps.nozzle2
      }
      ws.call(method, params)
    },
    setPosition: function (position) {
      var method = 'move_head_absolute'
      var params = {
        'x': position.x,
        'y': position.y,
        'z': position.z
      }
      ws.call(method, params)
    },
    homePrintHead: function (home) {
      var method = 'home_head'
      var params = {
        'x': !!home.x,
        'y': !!home.y,
        'z': !!home.z
      }
      ws.call(method, params)
    },
    retractFilament: function () {
      var method = 'retract_filament'
      var params = {
      }
      ws.call(method, params)
    },
    unretractFilament: function () {
      var method = 'unretract_filament'
      var params = {
      }
      ws.call(method, params)
    },
    printFile: function (fid) {
      if (printer.state === 'READY') {
        var method = 'print_gcode_file'
        var params = {
          'id': fid
        }
        ws.call(method, params)
      } else {
        console.log('cannot print because print file not ready')
      }
    },
    pausePrint: function () {
      var method = 'pause_print'
      var params = {
      }
      ws.call(method, params)
    },
    resumePrint: function () {
      var method = 'resume_print'
      var params = {
      }
      ws.call(method, params)
    },
    cancelPrint: function () {
      var method = 'cancel_print'
      var params = {
      }
      ws.call(method, params)
    },
    emergencyStop: function () {
      var method = 'emergency_stop'
      var params = {
      }
      ws.call(method, params)
    },
    putFile: function (file) {
      var vm = this
      var suc = function (f) {
        vm.getFile(f.id)
        printer.connection.printReady = true
      }
      var err = function () {
        printer.connection.printReady = false
      }
      var method = 'put_gcode_file'
      var params = {
        'name': file.name,
        'payload': file.contents
        // 'image': file.image,
        // 'meta': file.meta
      }
      ws.call(method, params, suc, err)
    },
    getFile: function (fid) {
      var suc = function (f) {
        printer.connection.printReady = true
        selectedFile.length = 0
        selectedFile.push(f)
      }
      var err = function () {
        printer.connection.printReady = false
        selectedFile.file = null
      }
      var method = 'get_gcode_file'
      var params = {
        'id': fid,
        'content': true
      }
      ws.call(method, params, suc, err)
    },
    getFiles: function () {
      var suc = function (d) {
        files.length = 0
        d['gcode_files'].forEach(
          function (f) {
            files.push(f)
          }
       )
      }
      ws.call('get_gcode_files', null, suc)
    },
    getCounters: function () {
      var suc = function (d) {
        counters.length = 0
        d['counters'].forEach(
          function (c, cid) {
            counters.push({ id: cid, val: c })
          }
       )
      }
      ws.call('get_counters', null, suc)
    },
    deselectFile: function () {
      this.selectedFile = null
    },
    connect: function () {
      connect()
    }
  }

  function connect () {
    ws = wsinst(printer.connection.baseUrl)
    /* ------------- BEGIN WEBSOCKET EVENTS ------------------ */
    ws.$on('state_change', function (message) {
      var params = message
      printer.state = params['new']
      console.log('state change event: ', message)

      if (params['old'] === 'EXECUTING' && params['new'] === 'READY') {
        printer.print.currentLine = null
        printer.print.totalLines = null
      }
    })

    ws.$on('temp_update', function (message) {
      var params = message
      printer.temperatures.bed.current = params.bed_current
      printer.temperatures.bed.target = params.bed_target
      printer.temperatures.nozzle1.current = params.nozzle1_current
      printer.temperatures.nozzle1.target = params.nozzle1_target
      printer.temperatures.nozzle2.current = params.nozzle2_current
      printer.temperatures.nozzle2.target = params.nozzle2_target
    })

    ws.$on('position_update', function (message) {
      var params = message
      printer.position.x = params.x
      printer.position.y = params.y
      printer.position.z = params.z
      console.log('position event: ', message)
    })

    ws.$on('progress_update', function (message) {
      var params = message
      printer.print.currentLine = params.current_line
      printer.print.totalLines = params.total_lines
      console.log('progress event: ', message)
    })
    /* ------------- END WEBSOCKET EVENTS ------------------ */
  }
  connect()
}
)(window)
