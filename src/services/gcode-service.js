(function (exports) {
  'use strict'

  exports.gcodeService = {
    version: "0.0.2",
    init: GCodeModel
  }

  function GCodeParser(handlers) {

    function delta(v1, v2) {
      return relative ? v2 : v2 - v1;
    };
    function absolute (v1, v2) {
      return relative ? v1 + v2 : v2;
    };

    this.handlers = handlers || {};

  };
  
  GCodeParser.prototype.parseLine = function(text, info) {

    var rename = {
            'Build time':'buildTime',
            'Filament length':'filamentLength',
            'Plastic weight':'plasticWeight',
            'Material cost':'materialCost'
          }

    if ( 0 == text.indexOf(';') ){
      var cmt 
      if( text.indexOf(',') > 0 ){
        cmt = text.replace(/;\s+/,'').split(',');
      }
      if( text.indexOf(':') > 0 ){
        cmt = text.replace(/;\s+/,'').split(':');
        cmt[0] = rename[cmt[0]] != null ? rename[cmt[0]] : cmt[0] ;
        cmt[1] = cmt[1] != null ? cmt[1].replace(/\s+/,'') : '' ;
      }
      if(cmt){
        var val2 = cmt[2] != null ? cmt[2] : null;
        var args = {tag:cmt[0],val:cmt[1],val2:val2};
          var handler = this.handlers['COMMENT'];
          if (handler) {
            return handler(args, info);
          }
      }
    }else{
      text = text.replace(/;.*$/, '').trim(); // Remove comments
      if (text) {
          var tokens = text.split(' ');
          if (tokens) {
            var cmd = tokens[0];
            var args = {
              'cmd': cmd
            };
            tokens.splice(1).forEach(function(token) {
              var key = token[0].toLowerCase();
              var value = parseFloat(token.substring(1));
              args[key] = value;
            });
            var handler = this.handlers[tokens[0]] || this.handlers['default'];
            if (handler) {
              return handler(args, info);
            }
          }
        }
    }

  };
  GCodeParser.prototype.parse = function(gcode) {
    var lines = gcode.split('\n');
    for (var i = 0; i < lines.length ; i++) {
      if (this.parseLine(lines[i], i) === false) {
        break;
      }
    }
  };

  function GCodeModel(txt) {

    // GCode descriptions come from:
    //    http://reprap.org/wiki/G-code
    //    http://en.wikipedia.org/wiki/G-code
    //    SprintRun source code

    // initialize variable for GCodeModel
    
      var layer = undefined;
      var gcm = this;
      gcm.layers = [];
      gcm.bbox = { min: { x:100000,y:100000,z:100000 }, max: { x:-100000,y:-100000,z:-100000 } };
    
      // adds new layer to GCodeModel.layers
      function newLayer(line) {
        layer = { type: {}, layer: gcm.layers.length, z: line.z, };
        gcm.layers.push(layer);
      };
      // takes line object in the form: {x:<xPos>,y:<yPos>,z:<zPos>,e:<ePos>,f:<feedRate>}
      // check to see if current layer exists, if not grab new Layer
      // calculate extruder 'speed' by dividing change in ePos by 1000
      // give grouptype 'id' value of 'speed' + 10000 if extruding is true
      // if layer.type[grouptype] exists, return it, otherwise create new layer.type[grouptype]
      function getLineGroup(line) {
        if (layer == undefined)
          newLayer(line);
        var speed = Math.round(line.e / 1000);
        var grouptype = (line.extruding ? 10000 : 0) + speed;
        if (layer.type[grouptype] == undefined) {
          layer.type[grouptype] = {
            type: grouptype,
            feed: line.e,
            extruding: line.extruding,
            geometry:{vertices:[]},
            segmentCount: 0
          }
        }
        return layer.type[grouptype];
      };
      // takes two lines in th form: {x:<xPos>,y:<yPos>,z:<zPos>,e:<ePos>,f:<feedRate>}
      // get linegroup for p2 (new point)
      // get geometry object from group
      // add another counter to segmentCount
      // push p1 vertices
      // push p2 vertices
    function addSegment(p1, p2) {
        var group = getLineGroup(p2);
        var geometry = group.geometry;
        
        group.segmentCount++;
        geometry.vertices.push({x:p1.x, y:p1.y, z:p1.z});
        geometry.vertices.push({x:p2.x, y:p2.y, z:p2.z});
        if (p2.extruding) {
          gcm.bbox.min.x = Math.min(gcm.bbox.min.x, p2.x);
          gcm.bbox.min.y = Math.min(gcm.bbox.min.y, p2.y);
          gcm.bbox.min.z = Math.min(gcm.bbox.min.z, p2.z);
          gcm.bbox.max.x = Math.max(gcm.bbox.max.x, p2.x);
          gcm.bbox.max.y = Math.max(gcm.bbox.max.y, p2.y);
          gcm.bbox.max.z = Math.max(gcm.bbox.max.z, p2.z);
        }
        if (gcm.bbox.min.x == 0){
          console.log(p2);
        }
    };

    var relative = false;
    function delta(v1, v2) {
        return relative ? v2 : v2 - v1;
    };
    function absolute (v1, v2) {
      return relative ? v1 + v2 : v2;
    };
    var lastLine = {x:0, y:0, z:0, e:0, f:0, extruding:false};
    var parseHandler = {    
                G1: function(args, line) {
                    // Example: G1 Z1.0 F3000
                    //          G1 X99.9948 Y80.0611 Z15.0 F1500.0 E981.64869
                    //          G1 E104.25841 F1800.0
                    // Go in a straight line from the current (X, Y) point
                    // to the point (90.6, 13.8), extruding material as the move
                    // happens from the current extruded length to a length of
                    // 22.4 mm.

                    var newLine = {
                      x: args.x !== undefined ? absolute(lastLine.x, args.x) : lastLine.x,
                      y: args.y !== undefined ? absolute(lastLine.y, args.y) : lastLine.y,
                      z: args.z !== undefined ? absolute(lastLine.z, args.z) : lastLine.z,
                      e: args.e !== undefined ? absolute(lastLine.e, args.e) : lastLine.e,
                      f: args.f !== undefined ? absolute(lastLine.f, args.f) : lastLine.f,
                    };
                    /* layer change detection is or made by watching Z, it's made by
                    watching when we extrude at a new Z position */
                    if (delta(lastLine.e, newLine.e) > 0 && newLine.x != 0 && newLine.y != 0 ) {
                      newLine.extruding = delta(lastLine.e, newLine.e) > 0;
                      if (layer == undefined || newLine.z != layer.z)
                        newLayer(newLine);
                    }
                    addSegment(lastLine, newLine);
                    lastLine = newLine;
                },

                G21: function(args) {
                    // G21: Set Units to Millimeters
                    // Example: G21
                    // Units from now on are in millimeters. (This is the RepRap default.)

                    // No-op: So long as G20 is not supported.
                },

                G90: function(args) {
                    // G90: Set to Absolute Positioning
                    // Example: G90
                    // All coordinates from now on are absolute relative to the
                    // origin of the machine. (This is the RepRap default.)

                    relative = false;
                },

                G91: function(args) {
                    // G91: Set to Relative Positioning
                    // Example: G91
                    // All coordinates from now on are relative to the last position.

                    // TODO!
                    relative = true;
                },

                G92: function(args) { // E0
                    // G92: Set Position
                    // Example: G92 E0
                    // Allows programming of absolute zero point, by reseting the
                    // current position to the values specified. This would set the
                    // machine's X coordinate to 10, and the extrude coordinate to 90.
                    // No physical motion will occur.

                    // TODO: Only support E0
                    var newLine = lastLine;
                    newLine.x= args.x !== undefined ? args.x : newLine.x;
                    newLine.y= args.y !== undefined ? args.y : newLine.y;
                    newLine.z= args.z !== undefined ? args.z : newLine.z;
                    newLine.e= args.e !== undefined ? args.e : newLine.e;
                    lastLine = newLine;
                },

                M82: function(args) {
                    // M82: Set E codes absolute (default)
                    // Descriped in Sprintrun source code.

                    // No-op, so long as M83 is not supported.
                },

                M84: function(args) {
                    // M84: Stop idle hold
                    // Example: M84
                    // Stop the idle hold on all axis and extruder. In some cases the
                    // idle hold causes annoying noises, which can be stopped by
                    // disabling the hold. Be aware that by disabling idle hold during
                    // printing, you will get quality issues. This is recommended only
                    // in between or after printjobs.

                    // No-op
                },

                COMMENT: function(args){
                    var tags = [
                            'printMaterial',
                            'printQuality',
                            'extruderName',
                            'filamentLength',
                            'plasticWeight'
                           ];

                    if(tags.indexOf(args.tag) >= 0){
                      gcm.meta = gcm.meta || {};
                      gcm.meta[args.tag] = args.val.split(' ')[0];
                    } else if ('buildTime' == args.tag){
                      gcm.meta['buildTime'] = '30000';
                    } else if ('temperatureName' == args.tag){
                      gcm.meta['temperatureName1'] = args.val;
                      gcm.meta['temperatureName2'] = args.val2;
                    } else if ('temperatureSetpointTemperatures' == args.tag){
                      gcm.meta[gcm.meta['temperatureName1']] = args.val;
                      gcm.meta[gcm.meta['temperatureName2']] = args.val2;
                    }
                },

                'default': function(args, info) {
                  // console.warn('Unknown command:', args.cmd, args, info);
                }
              };
  

    var parser = new GCodeParser(parseHandler);

    parser.parse(txt);

    return gcm;

  };  
}
)(window)
