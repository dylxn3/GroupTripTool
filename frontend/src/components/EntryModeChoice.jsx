function EntryModeChoice({ entryMode, setEntryMode, onNext, onBack }) {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
      <div className="flex items-center justify-between mb-1">
        <h2 className="text-lg font-semibold text-slate-900">
          How do you want to add travelers?
        </h2>
        <button
          onClick={onBack}
          className="text-sm text-slate-500 hover:text-slate-700"
        >
          ← Back
        </button>
      </div>
      <p className="text-sm text-slate-500 mb-4">
        You can always add more travelers later.
      </p>

      <div className="flex flex-col sm:flex-row gap-3">
        <button
          onClick={() => setEntryMode("planner")}
          className={`flex-1 border rounded-lg p-4 text-left transition-colors ${
            entryMode === "planner"
              ? "border-blue-500 bg-blue-50 ring-1 ring-blue-500"
              : "border-slate-300 hover:border-slate-400"
          }`}
        >
          <p className="font-medium text-slate-900">I'll enter everyone</p>
          <p className="text-slate-500 text-xs mt-1">
            Fastest — enter origins and people for the whole group yourself
          </p>
        </button>

        <button
          disabled
          className="flex-1 border border-slate-200 rounded-lg p-4 text-left opacity-50 cursor-not-allowed relative"
        >
          <span className="absolute top-2 right-2 text-[10px] font-semibold uppercase tracking-wide bg-slate-200 text-slate-500 px-1.5 py-0.5 rounded">
            Coming soon
          </span>
          <p className="font-medium text-slate-700">Send a link</p>
          <p className="text-slate-500 text-xs mt-1">
            Travelers enter their own info
          </p>
        </button>
      </div>

      <button
        onClick={onNext}
        disabled={!entryMode}
        className="mt-6 w-full bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed text-white font-medium px-4 py-2.5 rounded-lg transition-colors"
      >
        Continue
      </button>
    </div>
  );
}

export default EntryModeChoice;
