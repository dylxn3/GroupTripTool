function TravelerForm({ destination, setDestination }) {
  return (
    <div>
      <label className="block text-sm font-medium text-slate-700 mb-1.5">
        Destination
      </label>
      <input
        type="text"
        value={destination}
        onChange={(e) => setDestination(e.target.value)}
        placeholder="e.g. Cancun"
        className="w-full border border-slate-300 rounded-lg px-3 py-2 text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-shadow"
      />
    </div>
  );
}

export default TravelerForm;
