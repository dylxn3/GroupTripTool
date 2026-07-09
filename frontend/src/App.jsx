import { useState } from "react";
import TravelerForm from "./components/TravelerForm";
import TravelerList from "./components/TravelerList";
import Results from "./components/Results";

function App() {
  const [destination, setDestination] = useState("");
  const [originGroups, setOriginGroups] = useState([
    { origin: "", group_size: 1, budget: 0, currency: "USD" },
  ]);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const addOriginGroup = () => {
    setOriginGroups([
      ...originGroups,
      { origin: "", group_size: 1, budget: 0, currency: "USD" },
    ]);
  };

  const updateOriginGroup = (index, field, value) => {
    const updated = [...originGroups];
    updated[index][field] = value;
    setOriginGroups(updated);
  };

  const removeOriginGroup = (index) => {
    setOriginGroups(originGroups.filter((_, i) => i !== index));
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await fetch(
        "http://localhost:8000/check-affordability",
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ destination, origin_groups: originGroups }),
        },
      );

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">
        Group Trip Affordability Checker
      </h1>

      <TravelerForm destination={destination} setDestination={setDestination} />

      <TravelerList
        originGroups={originGroups}
        updateOriginGroup={updateOriginGroup}
        removeOriginGroup={removeOriginGroup}
        addOriginGroup={addOriginGroup}
      />

      <button
        onClick={handleSubmit}
        disabled={loading || !destination || originGroups.length === 0}
        className="mt-6 bg-blue-600 text-white px-4 py-2 rounded disabled:opacity-50"
      >
        {loading ? "Checking..." : "Check Affordability"}
      </button>

      {error && <p className="mt-4 text-red-600">Error: {error}</p>}

      {results && <Results results={results} />}
    </div>
  );
}

export default App;
