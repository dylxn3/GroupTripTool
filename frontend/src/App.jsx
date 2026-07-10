import { useState } from "react";
import TripBasicsForm from "./components/TripBasicsForm";
import EntryModeChoice from "./components/EntryModeChoice";
import OriginSetup from "./components/OriginSetup";
import OriginPeopleEntry from "./components/OriginPeopleEntry";
import Results from "./components/Results";

function App() {
  const [step, setStep] = useState(1);
  const [entryMode, setEntryMode] = useState(null);
  const [trip, setTrip] = useState({
    trip_name: "",
    destination_option: null,
    duration_days: null,
    date: "",
  });
  const [origins, setOrigins] = useState([]);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const updateTrip = (field, value) => setTrip({ ...trip, [field]: value });

  const addOrigin = (option) => {
    setOrigins((prev) => [
      ...prev,
      {
        origin_city_label: option.label,
        city_sky_id: option.sky_id,
        city_entity_id: option.entity_id,
        headcount: 0,
        entry_type: "individual",
        travelers: [],
        bulk_airport_sky_id: null,
        bulk_airport_entity_id: null,
        bulk_airport_label: null,
        bulk_budget: 0,
      },
    ]);
  };

  const removeOrigin = (index) =>
    setOrigins(origins.filter((_, i) => i !== index));

  const updateOrigin = (index, updatedOrigin) => {
    const updated = [...origins];
    updated[index] = updatedOrigin;
    setOrigins(updated);
  };

  const canSubmit =
    !loading &&
    origins.length > 0 &&
    trip.destination_option &&
    trip.date &&
    origins.every((o) => {
      if (o.headcount === 0) return false;
      if (o.entry_type === "individual") {
        return o.travelers.every((t) => t.name.trim() !== "" && t.budget > 0);
      }
      return o.bulk_budget > 0;
    });

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    setResults(null);

    const payload = {
      trip_name: trip.trip_name,
      destination_label: trip.destination_option?.label || "",
      destination_sky_id: trip.destination_option?.sky_id || null,
      destination_entity_id: trip.destination_option?.entity_id || null,
      duration_days: trip.duration_days,
      date: trip.date,
      origins,
    };

    console.log("Trip payload:", payload);

    try {
      const response = await fetch("http://localhost:8000/check-trip", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

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
    <div className="min-h-screen bg-slate-50 py-10 px-4">
      <div className="max-w-2xl mx-auto">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-slate-900">Coord</h1>
          <p className="text-slate-500 mt-2">
            Find travel plans that work for everyone.
          </p>
        </div>

        {step === 1 && (
          <TripBasicsForm
            trip={trip}
            updateTrip={updateTrip}
            onNext={() => setStep(2)}
          />
        )}

        {step === 2 && (
          <EntryModeChoice
            entryMode={entryMode}
            setEntryMode={setEntryMode}
            onNext={() => setStep(3)}
            onBack={() => setStep(1)}
          />
        )}

        {step === 3 && (
          <OriginSetup
            origins={origins}
            addOrigin={addOrigin}
            removeOrigin={removeOrigin}
            onNext={() => setStep(4)}
            onBack={() => setStep(2)}
          />
        )}

        {step === 4 && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-slate-900">
                Add People
              </h2>
              <button
                onClick={() => setStep(3)}
                className="text-sm text-slate-500 hover:text-slate-700"
              >
                ← Back
              </button>
            </div>

            {origins.map((origin, i) => (
              <OriginPeopleEntry
                key={i}
                origin={origin}
                updateOrigin={(updated) => updateOrigin(i, updated)}
              />
            ))}

            <button
              onClick={handleSubmit}
              disabled={!canSubmit}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed text-white font-medium px-4 py-2.5 rounded-lg transition-colors"
            >
              {loading ? "Checking..." : "Check Compatibility"}
            </button>

            {error && (
              <p className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
                Error: {error}
              </p>
            )}
          </div>
        )}

        {results && <Results results={results} />}
      </div>
    </div>
  );
}

export default App;
