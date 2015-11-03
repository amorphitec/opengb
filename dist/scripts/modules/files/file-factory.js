(function(angular) {

    'use strict';

    /* ----- BEGIN FUNCTION FOR FACTORY ----- */
    function factory(http) {

        var urlBase = 'api/file';
        var urlSuffix = '/file.json';

        var fileFactory = {};

        fileFactory.getFiles = function () {
            return http.get(urlBase + urlSuffix);
        };

        fileFactory.getFile = function (id) {
            return http.get(urlBase + '/' + id + urlSuffix);
        };

        fileFactory.insertFile = function (file) {
            //TODO: switch to actual http.post instead of faked get All 
            var files = http.get(urlBase+urlSuffix)
                                                    .success(function (files) {

                                                            files["4"] = file;

                                                        })
                                                        .error(function (error) {
                                                            console.log( 'Unable to load files data: ' + error );
                                                        });
            return files; 
//            return http.post(urlBase + urlSuffix, file);
        };

        fileFactory.updateFile = function (file) {
            return http.put(urlBase + '/' + file.id + urlSuffix, file);
        };

        fileFactory.deleteFile = function (id) {
            return http.delete(urlBase + '/' + id + urlSuffix);
        };

        return fileFactory;

    }
    /* ----- END FUNCTION FOR FACTORY ----- */

    angular
        .module('openGbApp')
        .factory('fileFactory', ['$http', factory]);

})(angular);        
