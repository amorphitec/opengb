(function(angular) {

  // TODO: move this from a factory to a constant
  // angular.module('ngGcode',[]).constant('gcode',null).config(['$provide',function($provide){}]);

  'use strict';

  function factory($document, $q, $rootScope){
      var d = $q.defer();
      function onScriptLoad() {
        // Load client in the browser
        $rootScope.$apply(function() { d.resolve(window.gcode); });
      }
      // Create a script tag with gcode.js as the source
      // and call our onScriptLoad callback when it
      // has been loaded
      var scriptTag = $document[0].createElement('script');
      scriptTag.type = 'text/javascript';
      scriptTag.async = true;
      scriptTag.src = 'scripts/lib/gcode/gcode.js';
      scriptTag.onreadystatechange = function () {
      if (this.readyState === 'complete') { onScriptLoad(); }
    };

    scriptTag.onload = onScriptLoad;

    var s = $document[0].getElementsByTagName('body')[0];
    s.appendChild(scriptTag);

    return {
      gcode: function() { return d.promise; },
    };
  };

  angular.module('gcode', [])
    .factory('gcodeService', ['$document', '$q', '$rootScope', factory ]);

})(angular);