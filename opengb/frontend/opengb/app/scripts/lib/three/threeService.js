(function(angular) {

  'use strict';

  function factory($document, $q, $rootScope){
    var d = $q.defer();

    function onScriptLoad() {
      // Load client in the browser
      var scriptTag2 = $document[0].createElement('script');
      scriptTag2.type = 'text/javascript';
      scriptTag2.async = true;
      scriptTag2.src = 'scripts/lib/three/TrackballControls.js';
      scriptTag2.onreadystatechange = function () {
        if (this.readyState === 'complete') { test2 = true;  onScriptLoad(); }
      };
      scriptTag2.onload = onScriptLoad2;
      var s = $document[0].getElementsByTagName('body')[0];
      s.appendChild(scriptTag2);
    };

    function onScriptLoad2() {
      // Load client in the browser
      $rootScope.$apply(function() { d.resolve(window.THREE); });
    };

    // Create a script tag with three as the source
    // and call our onScriptLoad callback when it
    // has been loaded
    var scriptTag = $document[0].createElement('script');
    scriptTag.type = 'text/javascript';
    scriptTag.async = true;
    scriptTag.src = 'scripts/lib/three/three.min.js';
    scriptTag.onreadystatechange = function () {
      if (this.readyState === 'complete') { test1 = true; onScriptLoad(); }
    };

    scriptTag.onload = onScriptLoad;

    var s = $document[0].getElementsByTagName('body')[0];
    s.appendChild(scriptTag);

    return {
      THREE: function() { return d.promise; },
    };

  };

  angular.module('three', [])
    .factory('threeService', ['$document', '$q', '$rootScope', factory]);

})(angular);