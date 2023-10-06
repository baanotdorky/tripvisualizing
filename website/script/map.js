function flyto(lat, long, zoom) {
  window.document.getElementById("main-map").firstElementChild.contentWindow.map_e87b5524d01ed2d6457568d067b6cee4.flyTo([lat, long],zoom);
}

var capeAlava = document.getElementById('cape-alava');
capeAlava.onclick = function() {flyto(48.16311873849357, -124.70171091520145, 12)};

var blueGlacier = document.getElementById('blue-glacier');
blueGlacier.onclick = function() {flyto(47.83898204591296, -123.7557950794418, 11)};

var enchantedValley = document.getElementById('enchanted-valley');
enchantedValley.onclick = function() {flyto(47.65944593234531, -123.40867926574853, 10.75)};

var highDivide = document.getElementById('high-divide');
highDivide.onclick = function() {flyto(47.92655057801194, -123.80008944052517, 12)};

var grandLoop = document.getElementById('grand-loop');
grandLoop.onclick = function() {flyto(47.926704128258145, -123.30802808632272, 11)};
