function Results({ results }) {
  return (
    <div className="mt-6 border-t pt-4">
      <h2 className="text-lg font-semibold mb-2">
        Results for {results.destination}
      </h2>

      {results.results.map((r, index) => (
        <div
          key={index}
          className={`p-3 rounded mb-2 ${
            r.error
              ? "bg-gray-100"
              : r.affordable
              ? "bg-green-100"
              : "bg-red-100"
          }`}
        >
          <p className="font-medium">{r.origin}</p>
          {r.error ? (
            <p className="text-sm text-gray-600">{r.error}</p>
          ) : (
            <>
              <p className="text-sm">
                Per-person budget: ${r.per_person_budget} — Fare: ${r.fare}
              </p>
              <p className="text-sm font-medium">
                {r.affordable ? "✅ Affordable" : `❌ Short by $${r.shortfall}`}
              </p>
            </>
          )}
        </div>
      ))}
    </div>
  );
}

export default Results;