import { useState } from "react";

function TripInput({ userId, onTripPlanned }) {
	const [source, setSource] = useState("");
	const [destination, setDestination] = useState("");
	const [budget, setBudget] = useState("");
	const [days, setDays] = useState("");
	const [peopleCount, setPeopleCount] = useState("");
	const [loading, setLoading] = useState(false);

	async function handleSubmit(e) {
		e.preventDefault();
		if (!userId) {
			alert("Missing user id");
			return;
		}

		setLoading(true);
		try {
			const res = await fetch(
				`http://localhost:8000/plan_trip?user_id=${userId}`,
				{
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({
						source,
						destination,
						budget: Number(budget),
						days: Number(days),
						people_count: Number(peopleCount),
					}),
				}
			);

			if (!res.ok) {
				alert("Failed to plan trip");
				return;
			}

			const data = await res.json();

			if (onTripPlanned) {
				onTripPlanned(data);
			}

			setSource("");
			setDestination("");
			setBudget("");
			setDays("");
			setPeopleCount("");
		} finally {
			setLoading(false);
		}
	}

	return (
		<form onSubmit={handleSubmit}>
			<h2>Plan a new trip</h2>
			<label>
				Source:{" "}
				<input
					value={source}
					onChange={(e) => setSource(e.target.value)}
					placeholder="From city"
				/>
			</label>
			<br />
			<label>
				Destination:{" "}
				<input
					value={destination}
					onChange={(e) => setDestination(e.target.value)}
					placeholder="To city"
				/>
			</label>
			<br />
			<label>
				Budget:{" "}
				<input
					type="number"
					value={budget}
					onChange={(e) => setBudget(e.target.value)}
					placeholder="Total budget"
				/>
			</label>
			<br />
			<label>
				Days:{" "}
				<input
					type="number"
					value={days}
					onChange={(e) => setDays(e.target.value)}
					placeholder="Number of days"
				/>
			</label>
			<br />
			<label>
				People count:{" "}
				<input
					type="number"
					value={peopleCount}
					onChange={(e) => setPeopleCount(e.target.value)}
					placeholder="Number of people"
				/>
			</label>
			<br />
			<button type="submit" disabled={loading}>
				{loading ? "Planning..." : "Plan trip"}
			</button>
		</form>
	);
}

export default TripInput;

