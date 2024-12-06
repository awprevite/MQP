require([
    "esri/Map",
    "esri/views/MapView",
    "esri/widgets/Search"
], function(Map, MapView, Search) {
    // Create the map with a basemap
    var map = new Map({
        basemap: "streets"  // You can change this to another basemap like "satellite" or "topo"
    });

    // Create the MapView to display the map in the "viewDiv" div
    var view = new MapView({
        container: "viewDiv", // ID of the HTML element to display the map
        map: map,             // The map instance
        center: [-118.805, 34.027], // Longitude, Latitude
        zoom: 13              // Zoom level
    });

    // Add a Search widget for user interaction
    var search = new Search({
        view: view
    });
    view.ui.add(search, "top-right"); // Add the search widget to the top-right corner of the map view
});
