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

  const canSubmit =
    !loading &&
    destination.trim() !== "" &&
    originGroups.length > 0 &&
    originGroups.every((g) => g.origin.trim() !== "" && g.budget > 0);

  return (
    <div className="min-h-screen bg-slate-50 py-10 px-4">
      <div className="max-w-2xl mx-auto">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-slate-900">
            Group Trip Coordinator
          </h1>
          <p className="text-slate-500 mt-2">
            See who can afford the trip, and by how much they're short if they
            can't.
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <TravelerForm
            destination={destination}
            setDestination={setDestination}
          />

          <TravelerList
            originGroups={originGroups}
            updateOriginGroup={updateOriginGroup}
            removeOriginGroup={removeOriginGroup}
            addOriginGroup={addOriginGroup}
          />

          <button
            onClick={handleSubmit}
            disabled={!canSubmit}
            className="mt-6 w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 active:bg-blue-800 disabled:bg-slate-300 disabled:cursor-not-allowed text-white font-medium px-4 py-2.5 rounded-lg transition-colors"
          >
            {loading && (
              <svg
                className="animate-spin h-4 w-4 text-white"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                ></path>
              </svg>
            )}
            {loading ? "Checking..." : "Check Affordability"}
          </button>

          {error && (
            <p className="mt-4 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
              Error: {error}
            </p>
          )}
        </div>

        {results && <Results results={results} />}
      </div>
    </div>
  );
}

export default App;
