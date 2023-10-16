let map = L.map('map').setView([46.63698077249043, -122.37537602527277], 10);
let polylines = new Array();

L.tileLayer(
            "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
            {"attribution": "\u0026copy; \u003ca href=\"https://www.openstreetmap.org/copyright\"\u003e" +
                    "OpenStreetMap\u003c/a\u003e contributors \u0026copy;\u003c" +
                    "a href=\"https://carto.com/attributions\"\u003eCARTO\u003c/a\u003e",
                "detectRetina": false,
                "maxNativeZoom": 18,
                "maxZoom": 18,
                "minZoom": 0,
                "noWrap": false,
                "opacity": 1,
                "subdomains": "abc",
                "tms": false}
            ).addTo(map);

function getTrips() {
    return new Promise(function(resolve,reject){
        fetch('JSON/trips.json')
            .then(response => response.json())
            .then(data => resolve(data))
    })
}

function displayTripButtons(trips) {
    for (let trip of trips) {
        // Create sidebar buttons
        const link = document.createElement("a");
        link.setAttribute("href", "#");
        link.setAttribute("id", trip.id);
        const div1 = document.createElement("div");
        const h2 = document.createElement("h2");
        div1.setAttribute("class", "trip-selection")
        const node = document.createTextNode(trip.name);
        h2.appendChild(node);
        div1.appendChild(h2);
        link.appendChild(div1);
        const element = document.getElementById("main-header");
        element.appendChild(link);
    }
}

function plotTrips(trips) {
    for (let trip of trips) {
        let latlng = JSON.parse(trip.latlng);
        let temp = L.polyline(latlng, {"bubblingMouseEvents": true, "color": "green", "dashArray": null, "dashOffset": null, "fill": false, "fillColor": "green", "fillOpacity": 0.2, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "noClip": false, "opacity": 0.5, "smoothFactor": 1.0, "stroke": true, "weight": 4.5}
                    );
        temp.addTo(map)
        let polyob = {
            id: trip.id,
            polyline: temp
        }
        polylines.push(polyob)
    }
}

function addEventListenersTrips(trips) {
    for (let trip of trips) {
        window.document.getElementById(trip.id).addEventListener("click", flyTo);
    }

}

function flyTo(evt) {
    let bounds = polylines.find(x => x.id == evt.currentTarget.getAttribute("id")).polyline.getBounds()
    map.flyToBounds(bounds);
}
getTrips()
    .then(function (trips) {
        displayTripButtons(trips);
        plotTrips(trips);
        addEventListenersTrips(trips);
    })


