function Results({ results }) {
  return (
    <div className="mt-6 bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <h2 className="text-lg font-semibold text-slate-900 mb-4">
        Results for <span className="text-blue-600">{results.destination}</span>
      </h2>

      <div className="space-y-4">
        {results.origin_results.map((o, index) => (
          <div key={index} className="border border-slate-200 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <p className="font-medium text-slate-900">{o.origin}</p>
              {o.error && (
                <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-slate-100 text-slate-500">
                  No route found
                </span>
              )}
            </div>

            {o.error ? (
              <p className="text-sm text-slate-500">{o.error}</p>
            ) : o.traveler_results ? (
              // Individual entry type
              <>
                <p className="text-sm text-slate-500 mb-2">
                  {o.compatible_count} of {o.total} can afford this — fare: $
                  {o.fare?.toFixed(0)}
                </p>
                <div className="space-y-1">
                  {o.traveler_results.map((t, i) => (
                    <div
                      key={i}
                      className={`flex items-center justify-between text-sm rounded px-2 py-1 ${
                        t.affordable ? "bg-green-50" : "bg-red-50"
                      }`}
                    >
                      <span>{t.name}</span>
                      <span
                        className={
                          t.affordable ? "text-green-700" : "text-red-700"
                        }
                      >
                        {t.affordable ? "Affordable" : `Short $${t.shortfall}`}
                      </span>
                    </div>
                  ))}
                </div>
              </>
            ) : (
              // Bulk entry type
              <div
                className={`text-sm rounded px-3 py-2 ${o.affordable ? "bg-green-50 text-green-700" : "bg-red-50 text-red-700"}`}
              >
                {o.headcount} people — fare: ${o.fare?.toFixed(0)} —{" "}
                {o.affordable
                  ? "Affordable for the group"
                  : `Short by $${o.shortfall} per person`}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Results;
