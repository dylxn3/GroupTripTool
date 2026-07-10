import { useState, useEffect, useRef } from "react";

function CityAutoComplete({ value, onSelect, cityOnly = false }) {
  const [query, setQuery] = useState(value?.label || "");
  const [options, setOptions] = useState([]);
  const [isHovering, setIsHovering] = useState(false);
  const [isFocused, setIsFocused] = useState(false);
  const debounceRef = useRef(null);

  useEffect(() => {
    if (query.length < 2) {
      setOptions([]);
      return;
    }

    clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(async () => {
      try {
        const res = await fetch(
          `http://localhost:8000/search-airports?query=${encodeURIComponent(query)}`,
        );
        const data = await res.json();
        let results = data.options || [];

        if (cityOnly) {
          results = results.filter((opt) => opt.entity_type === "CITY");
        }

        console.log("Fetched options:", results);
        setOptions(results);
      } catch (err) {
        console.error("Airport search failed:", err);
        setOptions([]);
      }
    }, 300);

    return () => clearTimeout(debounceRef.current);
  }, [query, cityOnly]);

  const handleSelect = (option) => {
    const cleanedOption = {
      ...option,
      label: option.label.replace(/\s*\(Any\)\s*$/i, ""),
    };
    setQuery(cleanedOption.label);
    setOptions([]);
    onSelect(cleanedOption);
  };

  const showDropdown = (isHovering || isFocused) && options.length > 0;

  return (
    <div
      className="relative w-full"
      onMouseEnter={() => setIsHovering(true)}
      onMouseLeave={() => setIsHovering(false)}
    >
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        placeholder="City"
        className="w-full border border-slate-300 rounded-md px-2.5 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      {showDropdown && (
        <ul className="absolute z-10 w-full bg-white border border-slate-200 rounded-md mt-1 shadow-lg max-h-48 overflow-y-auto">
          {options.map((opt) => (
            <li
              key={opt.sky_id + opt.entity_id}
              onMouseDown={(e) => {
                e.preventDefault();
                handleSelect(opt);
              }}
              className="px-3 py-1.5 text-sm hover:bg-blue-50 cursor-pointer"
            >
              {opt.label.replace(/\s*\(Any\)\s*$/i, "")}
              {!cityOnly && (
                <span className="text-xs text-slate-400 ml-1">
                  ({opt.entity_type})
                </span>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default CityAutoComplete;
