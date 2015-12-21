# opengb-ui

_Not yet ready for production use._


##Installation
_/dist contains the most recent version of the webapp_

to compile from source using bower/grunt:

	bower install

this will install the bower dependencies to /app/bower_components
	
	grunt build

/dist will be replaced with new build, including all bower dependencies.


###Modules

Material Design Template Directives: 

    <mdt-top-toolbar></mdt-top-toolbar>
    <mdt-navigation-menu></mdt-navigation-menu>

Printer UI Directives:

_Files_

	<og-file-search-list og-fsl-files="" 
		                 og-fsl-hide-empty="" 
		                 og-fsl-selected-file=""
		                 og-fsl-view="">
	</og-file-search-list>

	<og-file-dropbox og-fd-upload-file="">
	</og-file-dropbox>

    <og-file-image og-fi-file=""  
                   og-fi-height="" 
                   og-fi-width="" 
                   og-fi-circle="">
    </og-file-image>

    <og-gcode-viewer og-gcode-file="">
	</og-gcode-viewer>


_Controls_

	<controls-cube cc-x-pos=""  
				   cc-y-pos=""  
				   cc-z-pos=""  
				   cc-resolution="">
	</controls-cube>

Services:
	
	d3Service - wraps the d3.js library in an angular service to auto load/inject when used
	threeService - wraps the THREE.js library in an angular service to auto load/inject when used
	gcodeService - wraps a gcode library (based on /joewalnes/gcode-viewer) in an angular service to auto load/inject when used

