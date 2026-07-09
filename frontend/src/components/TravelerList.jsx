function TravelerList({ originGroups, updateOriginGroup, removeOriginGroup, addOriginGroup }) {
  return (
    <div className="mb-4">
      <label className="block font-medium mb-2">Origin Groups</label>

      {originGroups.map((group, index) => (
        <div key={index} className="flex gap-2 mb-2 items-center">
          <input
            type="text"
            placeholder="Origin city"
            value={group.origin}
            onChange={(e) => updateOriginGroup(index, "origin", e.target.value)}
            className="border rounded px-2 py-1 flex-1"
          />
          <input
            type="number"
            placeholder="Group size"
            value={group.group_size}
            min={1}
            onChange={(e) =>
              updateOriginGroup(index, "group_size", parseInt(e.target.value) || 1)
            }
            className="border rounded px-2 py-1 w-24"
          />
          <input
            type="number"
            placeholder="Budget"
            value={group.budget}
            min={0}
            onChange={(e) =>
              updateOriginGroup(index, "budget", parseFloat(e.target.value) || 0)
            }
            className="border rounded px-2 py-1 w-28"
          />
          <button
            onClick={() => removeOriginGroup(index)}
            className="text-red-600 px-2"
            type="button"
          >
            ✕
          </button>
        </div>
      ))}

      <button
        onClick={addOriginGroup}
        type="button"
        className="text-blue-600 mt-1 text-sm"
      >
        + Add origin group
      </button>
    </div>
  );
}

export default TravelerList;