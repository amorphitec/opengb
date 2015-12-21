(function(angular) {

    'use strict';

    function directive(d3Service) {
		
        /* ----- BEGIN LINK FUNCTION FOR DIRECTIVE ----- */
        function link(scope, element, attrs) {

                var vm = this;

                d3Service.d3().then(function(d3){

                    var dataSet = scope.dataSet;

                    var xmin = 0; 
                    var ymin = 0; 
                    var xmax = 0; 
                    var ymax = 0;

                    for (var series in dataSet ){
                        var data = dataSet[series];
                        for (var i = 0 ; i < data.length ; i++ ){
                            xmin = data[i].x < xmin ? data[i].x : xmin;
                            xmax = data[i].x > xmax ? data[i].x : xmax;
                            ymin = data[i].y < ymin ? data[i].y : ymin;
                            ymax = data[i].y > ymax ? data[i].y : ymax;
                        }
                    }

                    var x = d3.scale.linear()
                              .domain([xmin, xmax])  // the range of the values to plot
                              .range([ 0, element[0].scrollWidth ]);        // the pixel range of the x-axis

                    var y = d3.scale.linear()
                              .domain([ymin,ymax])
                              .range([ element[0].scrollHeight, 0 ]);

                    scope.grid = [];
                    for(var i = 0 ; i <= 6 ; i++ ){
                        var d = (xmax - xmin) * i / 6; 
                        scope.grid.push([{x:d,y:ymin},{x:d,y:ymax}]);
                    }
                    for(var i = 0 ; i <= 6 ; i++ ){
                        var d = (ymax - ymin) * i / 6; 
                        scope.grid.push([{x:xmin,y:d},{x:xmax,y:d}]);
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

                });

        }
        /* ----- END LINK FUNCTION FOR DIRECTIVE ----- */

        return {
            'restrict': 'E',
			'replace':true,
			'scope': {
				dataSet:'=tgDataSet'
            },
            'templateUrl': '/scripts/modules/statistics/directives/temperature-graph/temperature-graph-template.html',
            'link': link
        };

    }

    angular
        .module('openGbApp')
        .directive('ogTemperatureGraph', ['d3Service', directive] );

})(angular);