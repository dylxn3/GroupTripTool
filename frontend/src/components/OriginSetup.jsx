import { useState } from "react";
import CityAutoComplete from "./CityAutoComplete";

function OriginSetup({ origins, addOrigin, removeOrigin, onNext, onBack }) {
  const [pendingOption, setPendingOption] = useState(null);
  const [resetKey, setResetKey] = useState(0);

  const handleAdd = () => {
    if (!pendingOption) return;
    addOrigin(pendingOption);
    setPendingOption(null);
    setResetKey((k) => k + 1);
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <div className="flex items-center justify-between mb-1">
        <h2 className="text-lg font-semibold text-slate-900">
          Where are people coming from?
        </h2>
        <button
          onClick={onBack}
          className="text-sm text-slate-500 hover:text-slate-700"
        >
          ← Back
        </button>
      </div>
      <p className="text-sm text-slate-500 mb-4">
        Add every departure city or airport group involved in this trip.
      </p>

      <div className="flex flex-wrap gap-2 mb-4">
        {origins.map((o, i) => (
          <span
            key={i}
            className="flex items-center gap-1 bg-blue-50 text-blue-700 text-sm px-3 py-1 rounded-full"
          >
            {o.origin_city_label}
            <button
              onClick={() => removeOrigin(i)}
              className="text-blue-400 hover:text-blue-700"
            >
              ✕
            </button>
          </span>
        ))}
      </div>

      <div className="flex gap-2">
        <div className="flex-1">
          <CityAutoComplete
            key={resetKey}
            value={pendingOption}
            onSelect={setPendingOption}
            cityOnly
          />
        </div>
        <button
          onClick={handleAdd}
          type="button"
          disabled={!pendingOption}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed text-white px-4 rounded-lg text-sm"
        >
          Add
        </button>
      </div>

      <button
        onClick={onNext}
        disabled={origins.length === 0}
        className="mt-6 w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed text-white font-medium px-4 py-2.5 rounded-lg transition-colors"
      >
        Next: Add People
      </button>
    </div>
  );
}

export default OriginSetup;
