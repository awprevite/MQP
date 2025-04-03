import React, { useState } from "react";
import axios from "axios";
import "./globals.css";

const AddressSearch = ({ className, setUserCoordinates, setSearching, showNotification}) => {
  const [query, setQuery] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [debounceTimer, setDebounceTimer] = useState(null);

  // Fetch autocomplete suggestions
  const fetchSuggestions = (address) => {
    const api = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}&addressdetails=1&limit=5&countrycodes=us`;

    axios
      .get(api)
      .then((response) => {

        const filteredResults = response.data.filter(item => {
          const city = item.address?.city;
          const state = item.address?.state;
          return city === 'Worcester' && state === 'Massachusetts';
        });

        if (filteredResults.length > 0) {
          setSuggestions(filteredResults);
        } else {
          showNotification("No results found in Worcester, MA, try typing a more specific address");
          setSuggestions([]);
        }
      })
      .catch((error) => {
        console.error("Error fetching suggestions:", error);
      });
  };

  // Handle user input with debounce
  const handleInputChange = (event) => {
    const value = event.target.value;
    setQuery(value);

    // If the input length is greater than 2
    if (value.length > 2) {
      // Clear the previous timeout if user types again before 3 seconds
      if (debounceTimer) {
        clearTimeout(debounceTimer);
      }
      setSearching(true);

      // Set a new timeout to fetch suggestions after 3 seconds after the last input change
      const timer = setTimeout(() => {
        fetchSuggestions(value);
        setSearching(false);
      }, 2500); // 3 seconds delay

      setDebounceTimer(timer); // Store the timer to clear it later
    } else {
      setSuggestions([]);
      setSearching(false);
    }
  };

  // Handle selecting an address from suggestions
  const handleSelect = (address) => {
    const parts = address.display_name.split(", ");
    setQuery(`${parts[0]}, ${parts[1]}`); // Set input value to selected address
    setSuggestions([]); // Hide suggestions

    // Move map to selected address
    setUserCoordinates({ lat: address.lat, lng: address.lon });
  };

  return (
    <div>
      <input
        className={className}
        type='text'
        value={query}
        onChange={handleInputChange}
        placeholder={`search for ${className === "origin-input" ? "origin" : "destination"} address`}
      />

      {/* Autocomplete dropdown */}
      {suggestions.length > 0 && (
        <ul className={className === "origin-input" ? "origin-ul" : "destination-ul"}>
          {suggestions.map((item) => (
            <li 
              key={item.place_id} 
              onClick={() => handleSelect(item)}
              style={{ cursor: "pointer", padding: "5px" }}
            >
              {item.display_name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default AddressSearch;
