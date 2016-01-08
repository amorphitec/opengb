(function(angular) {

    'use strict';

    function directive(d3Service) {
		
        /* ----- BEGIN LINK FUNCTION FOR DIRECTIVE ----- */
        function link(scope, element, attrs) {

                var vm = this;

                scope.getSeries = function(series){
                    var arr = scope.dataSet[series].slice(0);
                    var data = [];
                    var s = Math.ceil(arr.length/100);
                    for(var i = 0 ; i < 100 ; i++){
                        var j = i * s;
                        if(j < arr.length){
                            data.push(arr[j]);
                        }
                    }
                    return data;
                };

                scope.$watch( 
                            function watchTemperatureData( scope ) {
                                return( scope.dataSet );
                            }, 
                            function handleSelectedFileChange( newValue, oldValue ){

                                if(newValue != null){

                                    d3Service.d3().then(function(d3){

                                        init();

                                    });
                                }
                            },
                            true
                );

                function init(){

                                    var dataSet = scope.dataSet;

                                    var xmin = 0; 
                                    var ymin = 0; 
                                    var xmax = 0; 
                                    var ymax = 0;

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
                }


        }
        /* ----- END LINK FUNCTION FOR DIRECTIVE ----- */

        return {
            'restrict': 'E',
            'templateNamespace': 'svg',
			'replace':true,
			'scope': {
				dataSet:'=tgDataSet'
            },
            'templateUrl': 'scripts/modules/statistics/directives/temperature-graph/temperature-graph-template.html',
            'link': link
        };

    }

    angular
        .module('openGbApp')
        .directive('ogTemperatureGraph', ['d3Service', directive] );

})(angular);