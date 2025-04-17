'use client'

import React, { useState, useRef, useEffect } from 'react';
import { useMapEvents } from 'react-leaflet';
import { Navigation, Moon, Square, SquareCheck, Minus } from 'lucide-react';
import dynamic from 'next/dynamic';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';
import './globals.css'
import { boundaryCoordinates, pointInPolygon } from './boundary';
import AddressSearch from './addressSearch';
import Loading from './loading';
import Welcome from './welcome';

// Dynamically import react-leaflet components, disabling SSR, avoid window is not defined issues
const MapContainer = dynamic(() => import('react-leaflet').then((mod) => mod.MapContainer), { ssr: false });
const TileLayer = dynamic(() => import('react-leaflet').then((mod) => mod.TileLayer), { ssr: false });
const GeoJSON = dynamic(() => import('react-leaflet').then((mod) => mod.GeoJSON), { ssr: false });
const CircleMarker = dynamic(() => import('react-leaflet').then((mod) => mod.CircleMarker), { ssr: false });

export default function Home() {

  // Active marker state
  const START_MARKER = 0;
  const END_MARKER = 1;
  const [currentMarker, setCurrentMarker] = useState(START_MARKER);

  // Notification state and logic
  const [notification, setNotification] = useState(null);
  const notificationTimeout = useRef(null);
  const notificationCounter = useRef(0);
  function showNotification(message) {
    setNotification(message + " (" + notificationCounter.current + ")");
    notificationCounter.current ++;

    if (notificationTimeout.current) {
      clearTimeout(notificationTimeout.current);
    }

    notificationTimeout.current = setTimeout(() => {
      setNotification(null);
      notificationTimeout.current = null;
    }, 3000);
  }

  // Clear address input states
  const [startAddressClear, setStartAddressClear] = useState(false);
  const [endAddressClear, setEndAddressClear] = useState(false);

  // Coordinate and time states, this is the info sent to the API
  const [startCoordinates, setStartCoordinates] = useState(null);
  const [endCoordinates, setEndCoordinates] = useState(null);
  const [time, setTime] = useState("");

  // Loading/searching states
  const [loading, setLoading] = useState(false);
  const [searching, setSearching] = useState(false);
  const [locating, setLocating] = useState(false);

  // Welcome screen state
  const [welcomeOpen, setWelcomeOpen] = useState(true);

  // Top menu of buttons state
  const [buttonsOpen, setButtonsOpen] = useState(true);
  const toggleButtonsOpen = () => {
    setButtonsOpen(!buttonsOpen);
  }

  // Route and route distance and time states
  const [geojsonData, setGeojsonData] = useState(null);
  const coolShapeLength = useRef(0);
  const coolTime = useRef(0);
  const [directGeojsonData, setDirectGeojsonData] = useState(null);
  const directShapeLength = useRef(0);
  const directTime = useRef(0);

  // Formatter for distances
  const formatter = new Intl.NumberFormat('en-US', {
    maximumFractionDigits: 2,
  });

  // Worcester boundary state, loaded on mount within use effect
  const [boundary, setBoundary ] = useState(null);
  useEffect(() => {
    fetch("/boundary.geojson")
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        setBoundary(data);
      })
  }, []);

  // Dark/light mode state
  const [darkMode, setDarkMode] = useState(false);
  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  }

  // Marker styles
  const startCircleStyle = {
    color: "lightgrey",   // Border color
    weight: 3,            // Border width
    fillColor: "#0A84FF", // Fill color
    fillOpacity: 1        // Fill opacity
  };
  const endCircleStyle = {
    color: "lightgrey",   // Border color
    weight: 3,            // Border width
    fillColor: "#EA4335", // Fill color
    fillOpacity: 1        // Fill opacity
  };

  // GeoJSON styles, routes and boundary
  const geojsonStyle = {
    color: "#0A84FF",     // Blue
    weight: 4,
    opacity: 0.6,
    fillOpacity: 0.6
  };
  const directGeojsonStyle = {
    color: "#EA4335",     // Red
    weight: 4,
    opacity: 0.8,
    fillOpacity: 0.7
  };
  const boundaryStyle = {
    color: darkMode ? "#8d8d8d" : "#000000",  // Grey or black
    weight: 5,
    opacity: 1,
    fillOpacity: 1
  };

  // Use the users current time and location upon mount
  useEffect(() => {
    let hours = new Date().getHours();
    if(hours < 6){
      hours = 6;
    } else if (hours > 20){
      hours = 20;
      setDarkMode(true);
    }
    hours.toString();
    setTime(hours);

    findLocation();
  }, []);

  // Function to find the user's location
  const findLocation = () => {
    setLocating(true);

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { latitude, longitude } = position.coords;

        // If valid response
        if (latitude && longitude) {
          const polygon = (boundaryCoordinates);
          const point = {lat: latitude, lng: longitude};

          // Check if the user is in Worcester
          if (pointInPolygon(point, polygon)) {
            setStartCoordinates({ lat: latitude, lng: longitude });
            fetchAddress(latitude, longitude);
          } else {
            showNotification("Must be in Worcester, MA, to use your location");
          }

        } else {
          showNotification("Unable to parse location coordinates")
        }
        setLocating(false);
      },
      (error) => {
        showNotification("Error getting location. Please enable location services");
        setLocating(false);
      }
    );
  };

  // Address states
  const [startAddress, setStartAddress] = useState("");
  const [endAddress, setEndAddress] = useState("");

  // Reverse geocoding to get address from coordinates
  const fetchAddress = (lat, lng) => {
    axios.get(`https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lng}`)
      .then((response) => {
        if(currentMarker === START_MARKER){
          setStartAddress(filterName(response.data));
        }else{
          setEndAddress(filterName(response.data));
        }
      })
      .catch((error) => {
        showNotification("Unable to find address");
      });
  };

  // ClickHandler component to handle marker placement on map tap
  const ClickHandler = () => {
    // Button menu must be open to place markers
    if(!buttonsOpen){
      return null;
    }
    useMapEvents({
      click: (e) => {
        const { lat, lng } = e.latlng;

        const polygon = (boundaryCoordinates);
        const point = {lat: lat, lng: lng};

        // Check if the clicked point is in Worcester
        if (pointInPolygon(point, polygon)) {

          // Update marker location based on selected marker
          if (currentMarker === START_MARKER) {
            setStartCoordinates({ lat, lng });
            setStartAddressClear(prev => !prev);
          } else {
            setEndCoordinates({ lat, lng });
            setEndAddressClear(prev => !prev);
          }

          // Find address for the clicked point
          fetchAddress(lat, lng);

        }else{
          showNotification("Please select a point within the boundary");
        }
      },
    });
    return null;
  };

  // Toggle marker between start and end
  const toggleMarker = (which) => {
    if (which === "start") {
      setCurrentMarker(START_MARKER);
    } else {
      setCurrentMarker(END_MARKER);
    }
  };
  const toggleMarkerStart = () => (currentMarker === START_MARKER ? "selected-start" : "regular");
  const toggleMarkerEnd = () => (currentMarker === END_MARKER ? "selected-end" : "regular");

  // Function to send coordinates to the API, response contains geojson data for the direct and cool route
  const sendCoordinatesToAPI = (e) => {

    // Check if has time and info for both markers
    if (!startCoordinates || !endCoordinates || time === "") {
      showNotification("Please place both start and end markers and select and a time");
      return;
    }

    setLoading(true);
    const coordinates = { start: startCoordinates, end: endCoordinates, time: time };

    axios.post("https://subtle-cowbird-elegant.ngrok-free.app/route", coordinates)
      .then((response) => {

        // Check if the direct route was returned with the correct data type
        if (response.data.direct_route && response.data.direct_route.type === "FeatureCollection") {
          setDirectGeojsonData(response.data.direct_route);
          directShapeLength.current = formatter.format(response.data.direct_route.features[0].properties.Shape_Leng/5280);
          directTime.current = Math.ceil(directShapeLength.current/0.0583);
        }

        // Check if the cool route was returned with the correct data type
        if (response.data.route && response.data.route.type === "FeatureCollection") {
          setGeojsonData(response.data.route);
          coolShapeLength.current = formatter.format(response.data.route.features[0].properties.Shape_Leng/5280);
          coolTime.current = Math.ceil(coolShapeLength.current/0.0583);
        }
      })
      .catch((error) => {
        showNotification("Error reaching the server");
      })
      .finally(() => {
        setLoading(false);
      });
  };

  // Cool and direct route toggles
  const [showCool, setShowCool] = useState(true);
  const [showDirect, setShowDirect] = useState(true);
  const toggleCool = () => {
    setShowCool(!showCool);
  }
  const toggleDirect = () => {
    setShowDirect(!showDirect);
  }

  // Address filters
  const filterName = (item) => {
    let address = "";
    if(item.address.leisure){
      address += item.address.leisure + ", ";
    }
    if(item.address.building){
      address += item.address.building + ", ";
    }
    if(item.address.amenity){
      address += item.address.amenity + ", ";
    }
    if(item.address.house_number){
      address += item.address.house_number + " ";
    }
    if(item.address.road){
      address += item.address.road + ", ";
    }
    if(item.address.city){
      address += item.address.city + ", ";
    }
    if(item.address.postcode){
      address += item.address.postcode;
    }

    return address.trim();
  }

  return (
    <>
      {welcomeOpen && <Welcome setWelcomeOpen={setWelcomeOpen} />}

      <div className='map-container'>
        {buttonsOpen &&
          <>
            <label className='set-label'>Use addresses OR tap the map to set <span className={currentMarker == START_MARKER ? 'blue':'red'}> {currentMarker == START_MARKER ? 'start':'end'}</span></label>
            <button className={`set-start-button ${toggleMarkerStart()}`} onClick={() => toggleMarker("start")}>Start</button>
            <button className={`set-end-button ${toggleMarkerEnd()}`} onClick={() => toggleMarker("end")}>End</button>
            <button className='calculate-button' onClick={sendCoordinatesToAPI} disabled={loading}>Go</button>
            <button className='locate-button' onClick={findLocation} disabled={locating}><Navigation size={18} /></button>
            <button className='dark-mode-button' onClick={toggleDarkMode}><Moon size={18} /></button>
            <AddressSearch className='start-input' clear={startAddressClear} setUserCoordinates={setStartCoordinates} setSearching={setSearching} showNotification={showNotification} address={startAddress} filterName={filterName}/>
            <AddressSearch className='end-input' clear={endAddressClear} setUserCoordinates={setEndCoordinates} setSearching={setSearching} showNotification={showNotification} address={endAddress} filterName={filterName}/>
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
          </>
        }

        <button className={buttonsOpen ? 'hide-buttons-button' : 'hide-buttons-button hidden'} onClick={toggleButtonsOpen}><Minus size={80} /></button>
        
        <button className='show-cool-checkbox' onClick={toggleCool}>{showCool ? <SquareCheck size={18} /> : <Square size={18} />}</button>
        <button className='show-direct-checkbox' onClick={toggleDirect}>{showDirect ? <SquareCheck size={18} /> : <Square size={18} />}</button>

        <MapContainer center={[42.2626, -71.8079]} zoom={13} style={{ height: "100%", width: "100%"} } zoomControl={false}>

          <TileLayer url={darkMode ? "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png" : "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png"} attribution='&copy; <a href="https://carto.com/attributions">CartoDB</a>'/>
          {showDirect && <GeoJSON key={`0-${directGeojsonData ? JSON.stringify(directGeojsonData) : 'empty'}`} data={directGeojsonData} style={directGeojsonStyle}/>}
          {showCool && <GeoJSON key={`1-${geojsonData ? JSON.stringify(geojsonData) : 'empty'}`} data={geojsonData} style={geojsonStyle}/>}
          <GeoJSON data={boundary} style={boundaryStyle}/>
          <ClickHandler />

          {startCoordinates && (<CircleMarker center={[startCoordinates.lat, startCoordinates.lng]} radius={10} pathOptions={startCircleStyle}></CircleMarker>)}
          {endCoordinates && (<CircleMarker center={[endCoordinates.lat, endCoordinates.lng]} radius={10} pathOptions={endCircleStyle}></CircleMarker>)}

        </MapContainer>

        {(loading || searching || locating) && 
          <Loading text={
            (loading && "calculate") ||
            (locating && "locate") ||
            (searching && "search") ||
            ""
            } 
          />}

        <label className='direct-info'>{directShapeLength.current} Miles<br />{directTime.current} Minutes</label>
        <label className='cool-info'>{coolShapeLength.current} Miles<br />{coolTime.current} Minutes</label>
      </div>

      {loading && <div className='loader'></div>}
      {searching && <div className='searcher'></div>}
      {locating && <div className='locator'></div>}
      {notification && (<div key={notification} className="notification">{notification.split("(")[0].trim()}</div>)}
    </>
  );
}
