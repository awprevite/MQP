'use client'

import React, { useState, useRef, useEffect } from "react";
import dynamic from "next/dynamic";
import { Marker, useMapEvents } from "react-leaflet";
import axios from "axios";
import "leaflet/dist/leaflet.css";
import "./globals.css"
import L from "leaflet";
import AddressSearch from "./addressSearch";
import { Navigation } from "lucide-react";
import { boundaryCoordinates, pointInPolygon } from "./boundary.js";

const customIconDestination = L.divIcon({
  className: '',
  html: '<div class=outer-circle><div class="inner-circle-white"></div></div>',
  iconSize: [20, 20],
  iconAnchor: [10, 10],
})

const customIconOrigin = L.divIcon({
  className: '',
  html: '<div class=outer-circle><div class="inner-circle-green"></div></div>',
  iconSize: [20, 20],
  iconAnchor: [10, 10],
})

// Dynamically import MapContainer and GeoJSON components, disabling SSR, Leaflet does not work with SSR
const MapContainer = dynamic(() => import('react-leaflet').then((mod) => mod.MapContainer), { ssr: false });
const TileLayer = dynamic(() => import('react-leaflet').then((mod) => mod.TileLayer), { ssr: false });
const GeoJSON = dynamic(() => import('react-leaflet').then((mod) => mod.GeoJSON), { ssr: false });

export default function Home() {

  const ORIGIN_MARKER = 0;
  const DESTINATION_MARKER = 1;

  const [notification, setNotification] = useState(null);

  function showNotification(message) {
    setNotification(message);

    setTimeout(() => {
      setNotification(null);
    }, 3000);
  }

  const [originCoordinates, setOriginCoordinates] = useState(null);
  const [destinationCoordinates, setDestinationCoordinates] = useState(null);
  const [currentMarker, setCurrentMarker] = useState(ORIGIN_MARKER);

  const [loading, setLoading] = useState(false);
  const [searching, setSearching] = useState(false);
  const [time, setTime] = useState("");

  const [geojsonData, setGeojsonData] = useState(null);
  const coolShapeLength= useRef(0);

  const [directGeojsonData, setDirectGeojsonData] = useState(null);
  const directShapeLength = useRef(0);

  const [boundary, setBoundary ] = useState(null);

  const formatter = new Intl.NumberFormat('en-US', {
    maximumFractionDigits: 2,  // Specify the number of decimal places
  });

  const geojsonStyle = {
    color: "green",
    weight: 5,
    opacity: 1,
    fillOpacity: 1
  };
  const directGeojsonStyle = {
    color: "black",
    weight: 5,
    opacity: 0.6,
    fillOpacity: 0.6
  };

  const boundaryStyle = {
    color: "black",
    weight: 5,
    opacity: 1,
    fillOpacity: 1
  };

  const findLocation = () => {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        if (latitude && longitude) {
          setOriginCoordinates({ lat: latitude, lng: longitude });
        } else {
          showNotification("Unable to parse location coordinates")
        }
      },
      (error) => {
        showNotification("Error getting location. Please enable location services");
      }
    );
  };

  // ClickHandler component to handle marker placement
  const ClickHandler = () => {
    useMapEvents({
      click: (e) => {
        const { lat, lng } = e.latlng;

        const polygon = (boundaryCoordinates);
        const point = {lat: lat, lng: lng};

        if (pointInPolygon(point, polygon)) {

          if (currentMarker === ORIGIN_MARKER) {
            setOriginCoordinates({ lat, lng });
          } else {
            setDestinationCoordinates({ lat, lng });
          }
        }else{
          showNotification("Please select a point within the boundary");
        }
      },
    });
  };

  // Toggle marker between start and end
  const toggleMarker = (which) => {
    if (which === "start") {
      setCurrentMarker(ORIGIN_MARKER);
    } else {
      setCurrentMarker(DESTINATION_MARKER);
    }
  };

  const toggleMarkerStart = () => (currentMarker === ORIGIN_MARKER ? "selected" : "regular");
  const toggleMarkerEnd = () => (currentMarker === DESTINATION_MARKER ? "selected" : "regular");

  const sendCoordinatesToAPI = (e) => {

    if (!originCoordinates || !destinationCoordinates || time === "") {
      showNotification("Please place both origin and destination markers and seclect and a time");
      return;
    }

    setLoading(true);

    const coordinates = { start: originCoordinates, end: destinationCoordinates, time: time };
    //console.log(coordinates);

    axios.post("http://127.0.0.1:5000/temp", coordinates)
      .then((response) => {
        //console.log("Data received successfully:", response.data);
        if (response.data.direct_route && response.data.direct_route.type === "FeatureCollection") {
          //console.log("Correct format")
          setDirectGeojsonData(response.data.direct_route);
          directShapeLength.current = formatter.format(response.data.direct_route.features[0].properties.Shape_Leng/5280);

        } else {
          //console.log("Invalid GeoJSON format or direct route does not exist");
        }
        if (response.data.route && response.data.route.type === "FeatureCollection") {
          //console.log("Correct format")
          setGeojsonData(response.data.route);
          coolShapeLength.current = formatter.format(response.data.route.features[0].properties.Shape_Leng/5280);

        } else {
          //console.log("Invalid GeoJSON format or route does not exist");
        }
      })
      .catch((error) => {
        //console.error("Error sending data:", error);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  useEffect(() => {
    fetch("/boundary.geojson")
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        setBoundary(data);
      })
      .catch((error) => {
        //console.error("Error fetching Boundary data:", error);
      });
  }, []);

  return (
    <>
      <div className='map-container'>
        <button className={`set-origin-button ${toggleMarkerStart()}`} onClick={() => toggleMarker("start")}>Set Origin</button>
        <button className={`set-destination-button ${toggleMarkerEnd()}`} onClick={() => toggleMarker("end")}>Set Destination</button>
        <button className='calculate-button' onClick={sendCoordinatesToAPI}>Calculate Route</button>
        <button className='locate-button' onClick={findLocation}><Navigation size={18} /></button>
        <select className='time-dropdown' value={time} onChange={(e) => setTime(e.target.value)}>
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
        <AddressSearch className='origin-input' setUserCoordinates={setOriginCoordinates} setSearching={setSearching} showNotification={showNotification}/>
        <AddressSearch className='destination-input' setUserCoordinates={setDestinationCoordinates} setSearching={setSearching} showNotification={showNotification}/>
        <MapContainer center={[42.2626, -71.8079]} zoom={13} style={{ height: "100%", width: "100%"} } zoomControl={false}>
          <TileLayer
            url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://carto.com/attributions">CartoDB</a>'
          />
          <GeoJSON key={`0-${directGeojsonData ? JSON.stringify(directGeojsonData) : 'empty'}`} data={directGeojsonData} style={directGeojsonStyle}/>
          <GeoJSON key={`1-${geojsonData ? JSON.stringify(geojsonData) : 'empty'}`} data={geojsonData} style={geojsonStyle}/>
          <GeoJSON data={boundary} style={boundaryStyle}/>
          <ClickHandler />
          {originCoordinates && (<Marker icon={customIconOrigin} position={[originCoordinates.lat, originCoordinates.lng]}></Marker>)}
          {destinationCoordinates && (<Marker icon={customIconDestination} position={[destinationCoordinates.lat, destinationCoordinates.lng]}></Marker>)}
        </MapContainer>
        <label className='direct-distance'>Direct Distance: {directShapeLength.current} Mi</label>
        <label className='cool-distance'>Cool Distance: {coolShapeLength.current} Mi</label>
      </div>
      {loading && <div className='loader'></div>}
      {searching && <div className='searcher'></div>}
      {notification && <div className="notification">{notification}</div>}
    </>
  );
}
