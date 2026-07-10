import { useState, useEffect } from "react";

function CityAirportPicker({ cityLabel, value, onSelect }) {
  const [airportOptions, setAirportOptions] = useState([]);

  useEffect(() => {
    if (!cityLabel) return;

    const fetchAirports = async () => {
      try {
        const res = await fetch(
          `http://localhost:8000/search-airports?query=${encodeURIComponent(cityLabel)}`,
        );
        const data = await res.json();
        // Only keep AIRPORT-type results (city-level "Any" option handled separately below)
        const airportsOnly = (data.options || []).filter(
          (o) => o.entity_type === "AIRPORT",
        );
        setAirportOptions(airportsOnly);
      } catch (err) {
        console.error("Failed to load airports for city:", err);
        setAirportOptions([]);
      }
    };

    fetchAirports();
  }, [cityLabel]);

  return (
    <select
      value={value?.sky_id || ""}
      onChange={(e) => {
        const selected = airportOptions.find(
          (o) => o.sky_id === e.target.value,
        );
        onSelect(selected || null); // null = "Any airport"
      }}
      className="w-full border border-slate-300 rounded-md px-2.5 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
    >
      <option value="">Choose an Airport </option>
      {airportOptions.map((opt) => (
        <option key={opt.sky_id} value={opt.sky_id}>
          {opt.label}
        </option>
      ))}
    </select>
  );
}

export default CityAirportPicker;
