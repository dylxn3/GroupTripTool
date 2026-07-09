function Results({ results }) {
  return (
    <div className="mt-6 bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <h2 className="text-lg font-semibold text-slate-900 mb-4">
        Results for <span className="text-blue-600">{results.destination}</span>
      </h2>

      <div className="space-y-3">
        {results.results.map((r, index) => (
          <div
            key={index}
            className={`rounded-lg border p-4 ${
              r.error
                ? "bg-slate-50 border-slate-200"
                : r.affordable
                  ? "bg-green-50 border-green-200"
                  : "bg-red-50 border-red-200"
            }`}
          >
            <div className="flex items-center justify-between">
              <p className="font-medium text-slate-900">{r.origin}</p>
              {!r.error && (
                <span
                  className={`text-xs font-semibold px-2 py-0.5 rounded-full ${
                    r.affordable
                      ? "bg-green-100 text-green-700"
                      : "bg-red-100 text-red-700"
                  }`}
                >
                  {r.affordable ? "Affordable" : "Short"}
                </span>
              )}
            </div>

            {r.error ? (
              <p className="text-sm text-slate-500 mt-1">{r.error}</p>
            ) : (
              <>
                <p className="text-sm text-slate-500 mt-1">
                  Per-person budget: ${r.per_person_budget.toFixed(0)} · Fare: $
                  {r.fare.toFixed(0)}
                </p>
                {!r.affordable && (
                  <p className="text-sm font-medium text-red-700 mt-1">
                    Short by ${r.shortfall.toFixed(0)} per person
                  </p>
                )}
              </>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Results;
