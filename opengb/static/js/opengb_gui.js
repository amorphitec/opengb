function switchContent(content) {
  $(".content").hide();
  console.log("." + content);
  $("#" + content).show();
} 

function parseMessage(message) {
  data = JSON.parse(message.data)
  if ("event" in data) {
    switch(data.event) {
      case 'temp':
        $("#bed-temp-current").text(data.params.bed_current);
        $("#bed-temp-target").text(data.params.bed_target);
        $("#nozzle1-temp-current").text(data.params.nozzle1_current);
        $("#nozzle1-temp-target").text(data.params.nozzle1_target);
        $("#nozzle2-temp-current").text(data.params.nozzle2_current);
        $("#nozzle2-temp-target").text(data.params.nozzle2_target);
        break;
      case 'state':
        $("#state").text(data.new);
        break;
      default:
        console.log('Could not parse message: ' + data);
    }
  } else {
    console.log(data.result);
  }
}

function setTemp() {
  var message = {
    'jsonrpc': '2.0',
    'id':       1,
    'method':   'set_temp',
    'params': {
      'bed':      105,
      'nozzle1':  206,
      'nozzle2':  203,
    }
  };
  socket.send(JSON.stringify(message)); 
}

function moveHead(x, y, z) {
  var message = {
    'jsonrpc': '2.0',
    'id':       1,
    'method':   'move_head',
    'params': {
      'x':  x,
      'y':  y,
      'z':  z,
    }
  };
  socket.send(JSON.stringify(message)); 
}

function getCounter() {
  var message = {
    'jsonrpc': '2.0',
    'id':       2,
    'method':  'get_counters',
    'params': {}
  };
  socket.send(JSON.stringify(message)); 
}
