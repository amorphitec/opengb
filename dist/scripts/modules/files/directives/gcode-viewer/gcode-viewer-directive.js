(function(angular) {

    'use strict';

    function directive(gcodeService,threeService) {

        /* ----- BEGIN LINK FUNCTION FOR DIRECTIVE ----- */
        function link(scope, element, attrs) {

            var vm = {};
            scope.progressMode = 'indeterminate';

            threeService.THREE().then(function(THREE){
                vm.THREE = THREE;

                //vm.scene = createScene();
                scope.progressMode = '';
//              zoomToFit();

            });

            scope.$watch( 
                            function watchSelectedFile( scope ) {
                                return( scope.file );
                            }, 
                            function handleSelectedFileChange( newValue, oldValue ){

                                if(newValue != null){

                                    scope.progressMode = 'indeterminate';

                                    // if(vm.scene && vm.renderer){
                                    //     vm.scene = null;
                                    //     vm.renderer.domElement.remove();
                                    //     vm.renderer = null;
                                    // }


                                    setTimeout(

                                                function(){

                                                    gcodeService.gcode().then(function(gcode){

                                                        vm.gcode = gcode.init(scope.file.contents);

                                                        scope.file.meta = scope.file.meta ? scope.file.meta : {};
                                                        for( var key in vm.gcode.meta){
                                                            if(!scope.file.meta[key]){
                                                                scope.file.meta[key] = vm.gcode.meta[key];
                                                            }
                                                        }
                                                                                                
                                                        console.log(scope.file);

                                                        threeService.THREE().then(function(THREE){
                                                            vm.THREE = vm.THREE != null ? vm.THREE : THREE;
                                                            vm.scene = vm.scene != null ? vm.scene : createScene();
                                                            vm.model = generateModel();
                                                            vm.scene.add(vm.model);
                                                            scope.progressMode = '';
                                                        });
                                                    });
                                                    
                                                },

                                                100
                                    );

                                }else{
                                    if(vm.scene){
                                        vm.scene.remove(vm.model);                                        
                                    }
                                }

            });

            function generateModel(){

                var layers = vm.gcode.layers;
                var bbox = vm.gcode.bbox;
                var THREE = vm.THREE;

                var object = new THREE.Object3D();
                    
                for (var lid in layers) {
                    var layer = layers[lid];

                    for (var tid in layer.type) {
                        var type = layer.type[tid];

                        var scale = 100 / layers.length;
                        var col = (type.extruding ? ( 0x006060 + Math.round( scale * lid ) * 0x000101 ) : 0x000000);
                        var mat = new THREE.LineBasicMaterial({
                                        color: col,
                                        opacity:type.extruding ? 1 : 0,
                                        transparency: false,
                                        linewidth: 3,
                                        vertexColors: THREE.VertexColors });

                        var geometry = new THREE.Geometry();
                        for (var i = 0; i < type.geometry.vertices.length; i++) {
                            var vect = type.geometry.vertices[i];
                            geometry.vertices.push( new THREE.Vector3(vect.x, vect.y, vect.z));
                            geometry.colors.push( new THREE.Color(col) );
                        }
                        

                        if(type.extruding){
                            object.add(new THREE.Line(geometry, mat, THREE.LineSegments));
                        }
                    }
                }

                // Center
                var scale = 1;

                var center = new THREE.Vector3(
                    bbox.min.x + ((bbox.max.x - bbox.min.x) / 2),
                    bbox.min.y + ((bbox.max.y - bbox.min.y) / 2),
                    bbox.min.z + ((bbox.max.z - bbox.min.z) / 2));
                console.log("center ", center);
                  
                object.position.x = -center.x*scale;
                object.position.y = -center.y*scale;
                console.log('position ', object.position);
                object.scale.multiplyScalar(scale);

                return object;
            };

            function createScene() {

                var THREE = vm.THREE;
                var controls;
                var width = element[0].scrollWidth;
                var height = element[0].scrollHeight;
                THREE.Object3D.DefaultUp = new THREE.Vector3( 0, 0, 1 );

                // Renderer
                vm.renderer = new THREE.WebGLRenderer({clearColor:0xFFFFFF, clearAlpha: 0, alpha:true});
                var renderer = vm.renderer;
                renderer.setSize(width,height);
                element.append(renderer.domElement);
                renderer.clear();

                // Scene
                var scene = new THREE.Scene(); 

                // Background
                var material = new THREE.MeshBasicMaterial( {color: 0xaaaaaa, side: THREE.DoubleSide, wireframe: true} );
                var sideWall = new THREE.PlaneGeometry( 1000, 1000, 10, 10 );
                var xMesh = new THREE.Mesh( sideWall, material )
                var yMesh = new THREE.Mesh( sideWall, material )
                var zMesh = new THREE.Mesh( sideWall, material )
                xMesh.rotation.y = Math.PI / 2 ;
                xMesh.position.x = 500;
                xMesh.position.z = 500;
                yMesh.rotation.x = Math.PI / 2 ;
                yMesh.position.y = 500;
                yMesh.position.z = 500;
                zMesh.rotation.z = Math.PI / 2 ;
                scene.add( xMesh );
                scene.add( yMesh );
                scene.add( zMesh );

                // Lights...
                [[0,0,1,  0xFFFFCC],
                [0,1,0,  0xFFCCFF],
                [1,0,0,  0xCCFFFF],
                [0,0,-1, 0xCCCCFF],
                [0,-1,0, 0xCCFFCC],
                [-1,0,0, 0xFFCCCC]].forEach(function(position) {
                    var light = new THREE.DirectionalLight(position[3]);
                    light.position.set(position[0], position[1], position[2]).normalize();
                    scene.add(light);
                });

                // Camera...
                var fov    = 30,
                    aspect = width/height,
                    near   = 1,
                    far    = 50000,
                    camera = new THREE.PerspectiveCamera(fov, aspect, near, far);

                camera.position.x = -3000;
                camera.position.y = -3000;
                camera.position.z = 3000;
                camera.lookAt(scene.position);
                scene.add(camera);
                controls = new THREE.TrackballControls(camera, element[0]);
                controls.noPan = true;
                controls.dynamicDampingFactor = 0.15;

                // Action!
                function render() {
                    controls.update();
                    renderer.render(scene, camera);
                    TWEEN.update();
                    requestAnimationFrame(render); // And repeat...
                }
                render();
                vm.camera = camera;

                return scene;
            };

            function zoomToFit(){

                var camera = vm.camera;
                var bbox = vm.gcode.bbox;

                var viewWidth = element[0].scrollWidth;
                var viewHeight = element[0].scrollHeight;
                var objWidth = bbox.max.x - bbox.min.x;
                var objHeight = bbox.max.y - bbox.min.y;
                var aspect = viewWidth / viewHeight;
                var sizes;

                if(viewWidth/objWidth < viewHeight/objHeight){
                    console.log('width');
                    sizes = [viewWidth,objWidth/aspect];
                }else{
                    console.log('height');
                    sizes = [viewHeight,objHeight];
                }

                if (sizes.length > 0){
                    
                    var dist = ( Math.min.apply(null, sizes) ) / 0.65;
                    new TWEEN.Tween(camera.position).to({y: -dist/1.4, z: dist/1.4, x: -dist/1.4}, 1000 ).start();

                }

            }

                    
        }
        /* ----- END LINK FUNCTION FOR DIRECTIVE ----- */

        return {
            'restrict': 'E',
			'replace':true,
			'scope': {
                'file': '=ogGcodeFile'
            },
            'template': '<div id="renderArea" ><og-file-image og-fi-file="file"></og-file-image><md-progress-circular md-mode="{{progressMode}}" md-diameter="100"></md-progress-circular></div>',
            'link': link
        };

    }

    angular
        .module('openGbApp')
        .directive('ogGcodeViewer', ['gcodeService', 'threeService', directive ]);

})(angular);