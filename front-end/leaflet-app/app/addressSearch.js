import React, { useState, useEffect } from "react";
import axios from "axios";
import "./globals.css";

const AddressSearch = ({ className, clear, setUserCoordinates, setSearching, showNotification, address, filterName}) => {

  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [debounceTimer, setDebounceTimer] = useState(null);

  // If address is updated from the map, update in the input
  useEffect(() => {
    setQuery(address);
  }, [address]);

  // If address is cleared, update in the input
  useEffect(() => {
    setQuery('');
    setSuggestions([]);
    if (debounceTimer) clearTimeout(debounceTimer);
  }, [clear]);

  // Fetch autocomplete suggestions
  const fetchSuggestions = (address) => {

    const api = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}&addressdetails=1&limit=5&countrycodes=us`;

    axios.get(api)
      .then((response) => {

        // Filter to include only results in Worcester, MA
        const filteredResults = response.data.filter(item => {
          const city = item.address?.city;
          const state = item.address?.state;
          return city === 'Worcester' && state === 'Massachusetts';
        });

        // If there are results, show them
        if (filteredResults.length > 0) {
          setSuggestions(filteredResults);
        } else {
          showNotification("No results found in Worcester, MA, try typing a more specific address");
          setSuggestions([]);
        }
      })
      .catch((error) => {
      });
  };

  // Handle user input with debounce
  const handleInputChange = (event) => {
    const value = event.target.value;
    setQuery(value);

    // Wait for atleast 3 characters to be entered, unlikely to find a match with less
    // Also wait for 1 seconds after the last input change to not flood the API with requests
    if (value.length > 2) {
      // Clear the previous timeout if user types again before 1 seconds
      if (debounceTimer) {
        clearTimeout(debounceTimer);
      }
      setSearching(true);

      // Set a new timeout to fetch suggestions after 1 seconds after the last input change
      const timer = setTimeout(() => {
        fetchSuggestions(value);
        setSearching(false);
      }, 1000);

      setDebounceTimer(timer);
    } else {
      setSuggestions([]);
      setSearching(false);
    }
  };

  // Handle selecting an address from suggestions
  const handleSelect = (item) => {
    // Set input value to selected address
    setQuery(filterName(item));
     // Hide suggestions
    setSuggestions([]);
    // Move marker to selected address
    setUserCoordinates({ lat: parseFloat(item.lat), lng: parseFloat(item.lon) });
  };

  return (
    <div style={{ position: "relative" }}>

      {/* Text area */}
      <input
        className={className}
        type='text'
        value={query}
        onChange={handleInputChange}
        placeholder={`search for ${className === "start-input" ? "start" : "end"} address`}
        onFocus={(e) => e.target.select()}
      />

      {/* Autocomplete dropdown */}
      {suggestions.length > 0 && (
        <ul className={className === "start-input" ? "start-ul" : "end-ul"}>
          {suggestions.map((item) => (
            <li key={item.place_id} onClick={() => handleSelect(item)} style={{ cursor: "pointer", padding: "5px" }}>
              {`${filterName(item)}`}
            </li>
          ))}
        </ul>
      )}

    </div>
  );
};

export default AddressSearch;