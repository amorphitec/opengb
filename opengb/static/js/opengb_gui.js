function switchContent(content) {
  $(".content").hide();
  console.log("." + content);
  $("#" + content).show();
} 

function parseMessage(message) {
  console.log(message.data)
  data = JSON.parse(message.data)
  switch(data.cmd) {
    case 'TEMP':
      $("#bed-temp").text(data.bed);
      $("#nozzle1-temp").text(data.nozzle1);
      $("#nozzle2-temp").text(data.nozzle2);
      break;
    case 'STATE':
      $("#state").text(data.new);
      break;
    default:
      console.log('Could not parse message: ' + data);
  }
}
