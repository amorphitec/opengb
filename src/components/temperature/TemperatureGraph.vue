<script>
  require('../../services/printer-service.js')
  var d3 = require('d3')

for (var series in dataSet ){
    var data = scope.getSeries(series);
    for (var i = 0 ; i < data.length ; i++ ){
        xmin = data[i].x < xmin ? data[i].x : xmin;
        xmax = data[i].x > xmax ? data[i].x : xmax;
        ymin = data[i].y < ymin ? data[i].y : ymin;
        ymax = data[i].y > ymax ? data[i].y : ymax;
    }
}

ymax = ymax * (1.2);

var x = d3.scale.linear()
          .domain([xmin, xmax])  // the range of the values to plot
          .range([ 0, element[0].scrollWidth ]);        // the pixel range of the x-axis

var y = d3.scale.linear()
          .domain([ymin,ymax])
          .range([ element[0].scrollHeight, 0 ]);

scope.grid = [];

var pow = Math.floor(Math.log(xmax) / Math.log(10));
pow = pow ? pow : 0 ;
// resMap should be 1sec < 10 seconds, 10 seconds < 100 seconds, 
var resMap = {
    0:2,
    1:10,
    2:60,
    3:600,
    4:7200,
    5:86400
};
var xRes = resMap[pow];
var xScale = 1;
var xLable = 'sec';


if(xmax > 4*60){
    xScale = 60;
    xLable = 'min';
} 
if (xmax > (2*60*60)){
    xScale = 60*60;
    xLable = 'hour';
}
if (xmax >= (1.5*24*60*60)){
    xScale = 24*60*60;
    xLable = 'day';
}


//SETUP GRID FOR X AXIS
var xGrid = Math.floor(xmax/xRes);
xGrid = xGrid > 0 ? xGrid : 1 ;

for(var i = 0 ; i <= xGrid ; i++ ){
    var d = xmin + (i * xRes); 
    var xL = Math.round((10*d/xScale))/10 + ' ' + xLable;
    var obj = {
                label:{x:d,y:0,text:xL},
                data:[
                        {x:d,y:ymin},
                        {x:d,y:ymax}
                     ]
              };
    scope.grid.push(obj);
}

//SETUP GRID FOR Y AXIS
var yRes = ymax > 100 ? 100 : 10;
var yGrid = Math.floor(ymax/yRes);
yGrid = yGrid > 0 ? yGrid : 1 ;

for(var i = 0 ; i <= yGrid; i++ ){
    var d = ymin + (i * yRes);
    var obj = {
                label:{x:0,y:d,text:d},
                data:[
                        {x:xmin,y:d},
                        {x:xmax,y:d}
                     ]
              }; 
    scope.grid.push(obj);
}

scope.settings = {x:x,y:y};
scope.line = d3.svg.line()
                .x(function(d) { return x(d.x); })
                .y(function(d) { return y(d.y); })
                .interpolate("none");

scope.curve = d3.svg.line()
                .x(function(d) { return x(d.x); })
                .y(function(d) { return y(d.y); })
                .interpolate("basis");
scope.x = x;
scope.y = y;

for (var series in dataSet ){
    var data = dataSet[series];
    for (var i = 0 ; i < data.length ; i++ ){
        dataSet[series][i].xPos = x(data[i].x);
        dataSet[series][i].yPos = y(data[i].y);
    }
}


  export default {
    data () {
      return {
        isHeating: false,
        printerService: printerws,
        xmin: 0,
        xmax: 0,
        ymin: 0,
        ymax: 0
      }
    },
    props: {
      value: '',
      name: ''
    },
    methods: {
    }
  }
</script>



<template>
<svg width="100%" height="100%">
  <g>
    <g data-ng-repeat="gridLine in grid">
      <path stroke="grey" 
          style="fill:none;stroke-width:2px"
          data-ng-attr-d="{{line(gridLine.data)}}">
      </path>
      <text data-ng-attr-x="{{x(gridLine.label.x)}}" 
          data-ng-attr-y="{{y(gridLine.label.y)}}" 
          fill="red">
          {{gridLine.label.text}}
      </text>
    </g>
  </g>
  <g data-ng-repeat="(series, data) in dataSet">
    <path data-ng-attr-stroke="{{series}}" 
          style="fill:none;stroke-width:3px;" 
        data-ng-attr-d="{{curve(getSeries(series))}}">
    </path>
  </g>
</svg>
</template>


<style>

</style>
