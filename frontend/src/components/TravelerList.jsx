function TravelerList({
  originGroups,
  updateOriginGroup,
  removeOriginGroup,
  addOriginGroup,
}) {
  return (
    <div className="mt-5">
      <label className="block text-sm font-medium text-slate-700 mb-1.5">
        Origin Groups
      </label>

      <div className="space-y-2">
        {originGroups.map((group, index) => (
          <div
            key={index}
            className="flex gap-2 items-center bg-slate-50 border border-slate-200 rounded-lg p-2"
          >
            <input
              type="text"
              placeholder="Origin City"
              value={group.origin}
              onChange={(e) =>
                updateOriginGroup(index, "origin", e.target.value)
              }
              className="flex-1 min-w-0 border border-slate-300 rounded-md px-2.5 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <input
              type="number"
              placeholder="# People"
              value={group.group_size === 0 ? "" : group.group_size}
              min={1}
              onChange={(e) => {
                const val = e.target.value;
                updateOriginGroup(
                  index,
                  "group_size",
                  val === "" ? "" : parseInt(val),
                );
              }}
              className="w-24 border border-slate-300 rounded-md px-2.5 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <div className="relative w-32">
              <span className="absolute left-2.5 top-1/2 -translate-y-1/2 text-slate-400 text-sm">
                $
              </span>
              <input
                type="number"
                placeholder="Total Budget for Group"
                value={group.budget === 0 ? "" : group.budget}
                min={0}
                onChange={(e) => {
                  const val = e.target.value;
                  updateOriginGroup(
                    index,
                    "budget",
                    val === "" ? "" : parseFloat(val),
                  );
                }}
                className="w-full border border-slate-300 rounded-md pl-5 pr-2.5 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <button
              onClick={() => removeOriginGroup(index)}
              type="button"
              disabled={originGroups.length === 1}
              className="shrink-0 h-8 w-8 flex items-center justify-center text-slate-400 hover:text-red-600 hover:bg-red-50 disabled:opacity-30 disabled:hover:bg-transparent disabled:hover:text-slate-400 rounded-md transition-colors"
              aria-label="Remove origin group"
            >
              ✕
            </button>
          </div>
        ))}
      </div>

      <button
        onClick={addOriginGroup}
        type="button"
        className="mt-3 text-sm font-medium text-blue-600 hover:text-blue-700 flex items-center gap-1"
      >
        <span className="text-base leading-none">+</span> Add origin group
      </button>
    </div>
  );
}

export default TravelerList;
