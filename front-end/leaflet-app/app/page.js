'use client'

import React, { useState, useEffect, useRef } from "react";
import dynamic from "next/dynamic"; // Import dynamic from next
import { Marker, Tooltip, useMapEvents } from "react-leaflet";
import axios from "axios";
import "leaflet/dist/leaflet.css";
import "./globals.css"
import L from "leaflet";

// Dynamically import MapContainer and GeoJSON components, disabling SSR
const MapContainer = dynamic(() => import('react-leaflet').then((mod) => mod.MapContainer), { ssr: false });
const TileLayer = dynamic(() => import('react-leaflet').then((mod) => mod.TileLayer), { ssr: false });
const GeoJSON = dynamic(() => import('react-leaflet').then((mod) => mod.GeoJSON), { ssr: false });

export default function Home() {
  
  useEffect(() => {
    if (typeof window !== "undefined") {
      const DefaultIcon = L.icon({
        iconUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
        shadowUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png",
        iconSize: [25, 41],
        iconAnchor: [12, 41],
      });
      L.Marker.prototype.options.icon = DefaultIcon;
    }
  }, []); 

  const MARKER_START = 0;
  const MARKER_END = 1;

  const [startMarker, setStartMarker] = useState(null);
  const [endMarker, setEndMarker] = useState(null);
  const [currentMarker, setCurrentMarker] = useState(MARKER_START);
  const [startCoordinateText, setStartCoordinateText] = useState("Start: Place Marker");
  const [endCoordinateText, setEndCoordinateText] = useState("End: Place Marker");
  const [geojsonData, setGeojsonData] = useState(null);
  const [directGeojsonData, setDirectGeojsonData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [time, setTime] = useState("");
  const geojsonLayerRef = useRef(null);

  const geojsonStyle = {
    color: "green",
    weight: 5,
    opacity: 0.6,
    fillOpacity: 0.5
  };
  const directGeojsonStyle = {
    color: "blue",
    weight: 5,
    opacity: 0.6,
    fillOpacity: 0.5
  }

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

  const sendCoordinatesToAPI = (e) => {

    if (!startMarker || !endMarker || time === "") {
      console.log("Both markers need to be placed on the map and a time must be entered before sending.");
      return;
    }

    setLoading(true);

    const coordinates = { start: startMarker, end: endMarker, time: time };
    console.log(coordinates);

    axios
      .post("http://127.0.0.1:5000/temp", coordinates)
      .then((response) => {
        console.log("Data received successfully:", response.data);
        if (response.data.direct_route && response.data.direct_route.type === "FeatureCollection") {
          console.log("Correct format")
          setDirectGeojsonData(response.data.direct_route);
        } else {
          setGeojsonData(null)
          console.log("Invalid GeoJSON format or direct route does not exist");
        }
        if (response.data.route && response.data.route.type === "FeatureCollection") {
          console.log("Correct format")
          setGeojsonData(response.data.route);
        } else {
          console.log("Invalid GeoJSON format or route does not exist");
        }
      })
      .catch((error) => {
        console.error("Error sending data:", error);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <div>
      <MapContainer center={[42.2626, -71.8079]} zoom={13} style={{ height: "100vh", width: "100%" }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution="&copy; OpenStreetMap contributors"
        />
        <GeoJSON key={`0-${directGeojsonData ? JSON.stringify(directGeojsonData) : 'empty'}`} data={directGeojsonData} style={directGeojsonStyle}/>
        <GeoJSON key={`1-${geojsonData ? JSON.stringify(geojsonData) : 'empty'}`} data={geojsonData} style={geojsonStyle}/>
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
          <label>Cool Routes Worcester</label>
          <button className={toggleMarkerStart()} onClick={() => toggleMarker("start")}>Set Start</button>
          <button className={toggleMarkerEnd()} onClick={() => toggleMarker("end")}>Set End</button>
          <select className='dropdown' value={time} onChange={(e) => setTime(e.target.value)}>
            <option value="" disabled>Select a time</option>
            <option value="6">6 am or earlier</option>
            <option value="7">7 am </option>
            <option value="8">8 am</option>
            <option value="9">9 am</option>
            <option value="10">10 am</option>
            <option value="11">11 am</option>
            <option value="12">12 pm</option>
            <option value="13">1 pm</option>
            <option value="14">2 pm</option>
            <option value="15">3 pm</option> 
            <option value="16">4 pm</option>
            <option value="17">5 pm</option>
            <option value="18">6 pm</option>
            <option value="19">7 pm</option>
            <option value="20">8 pm or later</option>
          </select>
          <button onClick={sendCoordinatesToAPI}>Calculate Route</button>
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
