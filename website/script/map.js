function flyto(evt) {
  window.document.getElementById("main-map").firstElementChild.contentWindow.eval(window.document.getElementById("main-map").firstElementChild.contentDocument.getElementsByClassName("folium-map")[0].id).flyTo([evt.currentTarget.getAttribute("lat"), evt.currentTarget.getAttribute("long")],10);
}

var trips;
fetch('JSON/trips.json')
  .then(response => response.json())
  .then(data => {
    trips = data;
    for(key in trips){
      const link = document.createElement("a");
      link.setAttribute("href","#");
      link.setAttribute("id",trips[key].leaflet_id);
      link.setAttribute("lat",trips[key].latitude_centroid);
      link.setAttribute("long",trips[key].longitude_centroid);
      const div1 = document.createElement("div");
      const h2 = document.createElement("h2");
      div1.setAttribute("class","trip-selection")
      const node = document.createTextNode(trips[key].name);
      h2.appendChild(node);
      div1.appendChild(h2);
      link.appendChild(div1);
      const element = document.getElementById("main-header");
      element.appendChild(link);
      console.log(trips[key].leaflet_id)
      window.document.getElementById(trips[key].leaflet_id).addEventListener("click", flyto);
    }
   }
   );







