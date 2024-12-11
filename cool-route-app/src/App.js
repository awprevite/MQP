// Filename - App.js

// Importing modules
import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, Polygon, Tooltip } from "react-leaflet";
import axios from "axios";
import "leaflet/dist/leaflet.css";
import "./App.css";
import L from 'leaflet';
import { useMapEvents } from "react-leaflet";
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

const DefaultIcon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});
L.Marker.prototype.options.icon = DefaultIcon;

function App() {
  const [markers, setMarkers] = useState([]);
  const [currentMarker, setCurrentMarker] = useState(0);

  // Function to handle click events on the map
  const ClickHandler = () => {
    useMapEvents({
      click: (e) => {
        const { lat, lng } = e.latlng;
        const newMarkers = [...markers];
        newMarkers[currentMarker] = { lat, lng };
        setMarkers(newMarkers);
        setCurrentMarker(currentMarker === 0 ? 1 : 0);
      },
    });
    return null;
  };

  // Function to send both coordinates to an API using axios
  const sendCoordinatesToAPI = () => {
    if (markers.length < 2 || !markers[0] || !markers[1]) {
      console.log("Both markers need to be placed on the map before sending.");
      return;
    }

    const coordinates = {
      start: markers[0], // First marker (start)
      end: markers[1], // Second marker (end)
    };

    // Replace 'YOUR_API_URL' with the actual API endpoint
    axios
      .post("http://127.0.0.1:5000/solve-route", coordinates)
      .then((response) => {
        console.log("Data sent successfully:", response.data);
      })
      .catch((error) => {
        console.error("Error sending data:", error);
      });
  };

  return (
    <div>
      <MapContainer center={[42.2626, -71.8079]} zoom={13} style={{ height: "100vh", width: "100%" }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />
        <ClickHandler /> {/* Handle clicks on the map */}

        {/* Render markers */}
        {markers.map(
          (position, index) =>
            position.lat && position.lng && (
              <Marker key={index} position={[position.lat, position.lng]}>
                <Tooltip direction="top" offset={[0, -15]} opacity={1}>
                  {index === 0 ? "Start" : "End"}
                </Tooltip>
              </Marker>
            )
        )}
      </MapContainer>

      <div className = "button-container">
        <button onClick={sendCoordinatesToAPI}>Send Coordinates</button>
      </div>
    </div>
  );

  /*
  // usestate for setting a javascript
  // object for storing and using data
  const [data, setdata] = useState({
    name: "",
    age: 0,
    date: "",
    programming: "",
  });

  // Using useEffect for single rendering
  useEffect(() => {
    // Using fetch to fetch the api from 
    // flask server it will be redirected to proxy
    fetch("/data").then((res) =>
      res.json().then((data) => {
        // Setting a data from api
        setdata({
          name: data.Name,
          age: data.Age,
          date: data.Date,
          programming: data.programming,
        });
      })
    );
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>React and flask</h1>
          { //Calling a data from setdata for showing}
          <p>{data.name}</p>
          <p>{data.age}</p>
          <p>{data.date}</p>
          <p>{data.programming}</p>

      </header>
    </div>
  );
  */
};

export default App;