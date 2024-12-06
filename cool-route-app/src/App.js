// Filename - App.js

// Importing modules
import React, { useState, useEffect } from "react";
import { MapContainer, TileLayer, Marker, Popup, Polygon } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import "./App.css";

function App() {
  const [point, setPoint] = useState(null);
  const [buffer, setBuffer] = useState(null);

  useEffect(() => {
    fetch("/point")
      .then((res) => res.json())
      .then((data) => setPoint(data.coordinates))
      .catch((err) => console.error("Failed to fetch point:", err));

    fetch("/buffer")
      .then((res) => res.json())
      .then((data) => setBuffer(data.coordinates))
      .catch((err) => console.error("Failed to fetch buffer:". err));
  }, []);

  return(
    <MapContainer center={[42.2626, -71.8079]} zoom={13} style={{ height: "100vh", width: "100%" }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="&copy; OpenStreetMap contributors"
      />
      {point && (
        <Marker position={[point[1], point[0]]}>
          <Popup>Point from ArcPy</Popup>
        </Marker>
      )}
      {buffer && (
        <Polygon positions={buffer} color="blue">
          <Popup>Buffer created with ArcPy</Popup>
        </Polygon>
      )}
    </MapContainer>
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