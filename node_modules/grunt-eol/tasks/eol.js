'use strict';
/*
 * grunt-eol
 * https://github.com/psyrendust/grunt-eol
 *
 * Copyright (c) 2013 Larry Gordon
 * Licensed under the MIT license.
 */


module.exports = function(grunt) {

  function getEOL(eol) {
    if (eol === 'lf') {
      return '\n';
    }
    if (eol === 'crlf') {
      return '\r\n';
    }
    return '\r';
  }

  grunt.registerMultiTask('eol', 'Convert line endings the easy way.', function() {
    var done = this.async();

    // Merge task-specific and/or target-specific options with these defaults.
    var options = this.options({
      eol: 'lf',
      replace: false
    });

    // Iterate over all specified file groups.
    this.files.forEach(function(f) {
      var eol = getEOL(options.eol);
      var message = (options.replace) ? 'Creating file ' : 'Replacing file ';
      f.src.filter(function(filepath) {
        // Warn on and remove invalid source files (if nonull was set).
        if (!grunt.file.exists(filepath)) {
          grunt.log.warn('Source file "' + filepath + '" not found.');
          return false;
        } else {
          return true;
        }
      }).forEach(function(filepath) {
        if (grunt.file.isFile(filepath)) {
          var file = grunt.file.read(filepath);
          var destination = f.dest;
          file = file.replace(/\r\n|\n|\r/g, eol);
          // Replace the destination file
          if (options.replace) {
            destination = filepath;
          }
          // Write the destination file.
          grunt.log.write(message.cyan + destination + '...');
          grunt.file.write(destination, file);
          grunt.log.ok();
        }
      });
    });

    done();
  });

};
