function TravelerForm({ destination, setDestination }) {
  return (
    <div className="mb-4">
      <label className="block font-medium mb-1">Destination</label>
      <input
        type="text"
        value={destination}
        onChange={(e) => setDestination(e.target.value)}
        placeholder="e.g. Cancun"
        className="border rounded px-3 py-2 w-full"
      />
    </div>
  );
}

export default TravelerForm;