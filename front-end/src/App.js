import React, { useState, useEffect, useRef } from "react";
import { MapContainer, TileLayer, Marker, Tooltip, useMapEvents, GeoJSON } from "react-leaflet";
import axios from "axios";
import "leaflet/dist/leaflet.css";
import "./App.css";
import L from "leaflet";

const DefaultIcon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});
L.Marker.prototype.options.icon = DefaultIcon;

const MARKER_START = 0;
const MARKER_END = 1;

function App() {
  const [startMarker, setStartMarker] = useState(null);
  const [endMarker, setEndMarker] = useState(null);
  const [currentMarker, setCurrentMarker] = useState(MARKER_START);
  const [startCoordinateText, setStartCoordinateText] = useState("Start: Place Marker");
  const [endCoordinateText, setEndCoordinateText] = useState("End: Place Marker");
  const [geoJsonData, setGeoJsonData] = useState(null);
  const [loading, setLoading] = useState(false);

  const geoJsonLayerRef = useRef();

  useEffect(() => {
    if (geoJsonData && geoJsonLayerRef.current) {
      geoJsonLayerRef.current.clearLayers();
      geoJsonLayerRef.current.addData(geoJsonData);
    }
  }, [geoJsonData]);


  const polygon = L.polygon([
    [42.20, -71.90],  // Southwest corner, just outside Worcester to the west
    [42.20, -71.70],  // Southeast corner, just outside Worcester to the east
    [42.34, -71.70],  // Northeast corner, just outside Worcester to the north
    [42.34, -71.90],  // Northwest corner, just outside Worcester to the north-west
    [42.20, -71.90]   // Closing the polygon
  ]);  

  // ClickHandler component to handle marker placement
  const ClickHandler = () => {
    useMapEvents({
      click: (e) => {
        const { lat, lng } = e.latlng;
        const point = L.latLng(lat, lng);

        if (polygon.getBounds().contains(point)) {

          if (currentMarker === MARKER_START) {
            setStartMarker({ lat, lng });
            setStartCoordinateText(`Start: ${lat.toFixed(6)}, ${lng.toFixed(6)}`);
          } else {
            setEndMarker({ lat, lng });
            setEndCoordinateText(`End: ${lat.toFixed(6)}, ${lng.toFixed(6)}`);
          }
        }else{
          console.log("clicked too far away")
        }
      },
    });
    return null;
  };

  // Toggle marker between start and end
  const toggleMarker = (which) => {
    if (which === "start") {
      setCurrentMarker(MARKER_START);
    } else {
      setCurrentMarker(MARKER_END);
    }
  };

  const toggleMarkerStart = () => (currentMarker === MARKER_START ? "selected" : "regular");
  const toggleMarkerEnd = () => (currentMarker === MARKER_END ? "selected" : "regular");

  const sendCoordinatesToAPI = () => {
    if (!startMarker || !endMarker) {
      console.log("Both markers need to be placed on the map before sending.");
      return;
    }

    setLoading(true);

    const coordinates = { start: startMarker, end: endMarker };
    console.log(coordinates);

    axios
      .post("http://127.0.0.1:5000/temp", coordinates)
      .then((response) => {
        console.log("Data received successfully:", response.data);
        if (response.data.type === "FeatureCollection") {
          console.log("Correct format")
          //setGeoJsonData(response.data);
        } else {
          console.error("Invalid GeoJSON format");
        }
      })
      .catch((error) => {
        console.error("Error sending data:", error);
      })
      .finally(() => {
        setLoading(false);
      });
  };
  
  useEffect(() => {
    // Fetch the GeoJSON file from the public folder
    fetch("/RouteOutputConverted.geojson")
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        setGeoJsonData(data);
      })
      .catch((error) => {
        console.error("Error loading GeoJSON file:", error);
      });
  }, []);
  

  return (
    <div>
      <MapContainer center={[42.2626, -71.8079]} zoom={13} style={{ height: "100vh", width: "100%" }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />
        {geoJsonData && <GeoJSON data={geoJsonData} />}
        <ClickHandler />
        {startMarker && (
          <Marker position={[startMarker.lat, startMarker.lng]}>
            <Tooltip direction="top" offset={[0, -15]} opacity={1}>
              Start
            </Tooltip>
          </Marker>
        )}
        {endMarker && (
          <Marker position={[endMarker.lat, endMarker.lng]}>
            <Tooltip direction="top" offset={[0, -15]} opacity={1}>
              End
            </Tooltip>
          </Marker>
        )}
      </MapContainer>
      <div className='panel'>
        <div className='left-button-container'>
          <button className={toggleMarkerStart()} onClick={() => toggleMarker("start")}>
            Set Start
          </button>
          <button className={toggleMarkerEnd()} onClick={() => toggleMarker("end")}>
            Set End
          </button>
          <button onClick={sendCoordinatesToAPI}>Send Coordinates</button>
          {loading &&
            <div className='loader'></div>
          }
        </div>
      </div>
      <div className="button-container">
        <div>
          <label>{startCoordinateText}</label>
        </div>
        <div>
          <label>{endCoordinateText}</label>
        </div>
      </div>
    </div>
  );
}

export default App;
