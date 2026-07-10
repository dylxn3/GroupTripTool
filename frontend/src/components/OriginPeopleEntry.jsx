import CityAirportPicker from "./CityAirportPicker";

function OriginPeopleEntry({ origin, updateOrigin }) {
  const setHeadcount = (val) => {
    const count = parseInt(val) || 0;
    const entryType = count > 10 ? "bulk" : "individual";

    let travelers = origin.travelers;
    if (entryType === "individual") {
      travelers = Array.from(
        { length: count },
        (_, i) =>
          origin.travelers[i] || {
            name: "",
            budget: 0,
            airport_sky_id: null,
            airport_entity_id: null,
            airport_label: null,
          },
      );
    }

    updateOrigin({
      ...origin,
      headcount: count,
      entry_type: entryType,
      travelers,
    });
  };

  const updateTraveler = (i, field, value) => {
    const updated = [...origin.travelers];
    updated[i][field] = value;
    updateOrigin({ ...origin, travelers: updated });
  };

  const updateTravelerAirport = (i, opt) => {
    const updated = [...origin.travelers];
    updated[i] = {
      ...updated[i],
      airport_sky_id: opt?.sky_id || null,
      airport_entity_id: opt?.entity_id || null,
      airport_label: opt?.label || null,
    };
    updateOrigin({ ...origin, travelers: updated });
  };

  return (
    <div className="bg-slate-50 border border-slate-200 rounded-lg p-4">
      <p className="font-medium text-slate-900 mb-2">
        {origin.origin_city_label}
      </p>

      <div className="mb-3">
        <label className="block text-xs font-medium text-slate-600 mb-1">
          How many people from this city?
        </label>
        <input
          type="number"
          min={1}
          placeholder="# people"
          value={origin.headcount || ""}
          onChange={(e) => setHeadcount(e.target.value)}
          className="w-28 border border-slate-300 rounded-md px-2.5 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      {origin.headcount > 0 && origin.entry_type === "individual" && (
        <div className="space-y-2">
          <p className="text-xs text-slate-500">
            10 or fewer — enter each person individually
          </p>
          {origin.travelers.map((t, i) => (
            <div
              key={i}
              className="flex flex-col gap-1.5 bg-white border border-slate-200 rounded-md p-2"
            >
              <div className="flex gap-2">
                <input
                  placeholder={`Name of Person ${i + 1}`}
                  value={t.name}
                  onChange={(e) => updateTraveler(i, "name", e.target.value)}
                  className="flex-1 border border-slate-300 rounded-md px-2.5 py-1.5 text-sm"
                />
                <div className="relative w-28">
                  <span className="absolute left-2.5 top-1/2 -translate-y-1/2 text-slate-400 text-sm">
                    $
                  </span>
                  <input
                    type="number"
                    placeholder="Budget"
                    value={t.budget === 0 ? "" : t.budget}
                    onChange={(e) =>
                      updateTraveler(
                        i,
                        "budget",
                        e.target.value === "" ? "" : parseFloat(e.target.value),
                      )
                    }
                    className="w-full border border-slate-300 rounded-md pl-5 pr-2.5 py-1.5 text-sm"
                  />
                </div>
              </div>
              <div>
                <p className="text-[11px] text-slate-400 mb-1">Flying from:</p>
                <CityAirportPicker
                  cityLabel={origin.origin_city_label}
                  value={
                    t.airport_sky_id
                      ? { sky_id: t.airport_sky_id, label: t.airport_label }
                      : null
                  }
                  onSelect={(opt) => updateTravelerAirport(i, opt)}
                />
              </div>
            </div>
          ))}
        </div>
      )}

      {origin.headcount > 10 && origin.entry_type === "bulk" && (
        <div className="space-y-2">
          <p className="text-xs text-slate-500 mb-1">
            More than 10 — enter one shared per-person budget for this group
          </p>
          <div className="relative w-32">
            <span className="absolute left-2.5 top-1/2 -translate-y-1/2 text-slate-400 text-sm">
              $
            </span>
            <input
              type="number"
              placeholder="Budget/person"
              value={origin.bulk_budget || ""}
              onChange={(e) =>
                updateOrigin({
                  ...origin,
                  bulk_budget: parseFloat(e.target.value) || 0,
                })
              }
              className="w-full border border-slate-300 rounded-md pl-5 pr-2.5 py-1.5 text-sm"
            />
          </div>
          <div>
            <p className="text-[11px] text-slate-400 mb-1">Flying from:</p>
            <CityAirportPicker
              cityLabel={origin.origin_city_label}
              value={
                origin.bulk_airport_sky_id
                  ? {
                      sky_id: origin.bulk_airport_sky_id,
                      label: origin.bulk_airport_label,
                    }
                  : null
              }
              onSelect={(opt) =>
                updateOrigin({
                  ...origin,
                  bulk_airport_sky_id: opt?.sky_id || null,
                  bulk_airport_entity_id: opt?.entity_id || null,
                  bulk_airport_label: opt?.label || null,
                })
              }
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default OriginPeopleEntry;
