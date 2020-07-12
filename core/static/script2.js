
var initialCoordinates = [-5.11, -42.75]; // Rio de Janeiro
var initialZoomLevel = 13;



// create a map in the "map" div, set the view to a given place and zoom
var map = L.map('map1').setView(initialCoordinates, initialZoomLevel);


// add an OpenStreetMap tile layer
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; Contribuidores do <a href="http://osm.org/copyright">OpenStreetMap</a>'
}).addTo(map);




var planes = [
		["João",-5.1133557,-42.7585415],
		["Pedro",-5.1137061,-42.7633573],
		["Caio",-5.110676,-42.7587106],
		["Irvyane", -5.1025297,-42.7562946],
		["Neto", -5.100072,-42.7499904]

		];








