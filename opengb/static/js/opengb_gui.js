function switchContent(content) {
  $(".content").hide();
  console.log("." + content);
  $("#" + content).show();
} 

function updateStatus() {
  console.log('updating status');
  $.getJSON( "api/status", function( data ) {
    $("#status").text(data['state']);
    $("#bed-temp").text(data['temp']['bed']);
    console.log(data);
  });
}
