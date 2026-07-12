import CityAutoComplete from "./CityAutoComplete";

function TripBasicsForm({ trip, updateTrip, onNext }) {
  const canProceed = trip.trip_name.trim() !== "" && trip.date !== "";

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <h2 className="text-lg font-semibold text-slate-900 mb-4">Trip Basics</h2>

      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1.5">
            Trip Name <span className="text-red-500">*</span>
          </label>
          <input
            type="text"
            value={trip.trip_name}
            onChange={(e) => updateTrip("trip_name", e.target.value)}
            placeholder="e.g. Japan Trip 2027"
            className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1.5">
            Destination{" "}
            <span className="text-slate-400 font-normal">
              (optional — leave blank to explore anywhere)
            </span>
          </label>
          <CityAutoComplete
            value={trip.destination_option}
            onSelect={(opt) => updateTrip("destination_option", opt)}
            cityOnly
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1.5">
              Duration (days)
            </label>
            <input
              type="number"
              min={1}
              value={trip.duration_days || ""}
              onChange={(e) =>
                updateTrip("duration_days", parseInt(e.target.value) || null)
              }
              placeholder="7"
              className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1.5">
              Target Date <span className="text-red-500">*</span>
            </label>
            <input
              type="date"
              value={trip.date || ""}
              onChange={(e) => updateTrip("date", e.target.value)}
              className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>

      <button
        onClick={onNext}
        disabled={!canProceed}
        className="mt-6 w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed text-white font-medium px-4 py-2.5 rounded-lg transition-colors"
      >
        Next
      </button>
    </div>
  );
}

export default TripBasicsForm;
