def search_hotels():
	avg_night_budget = 1800 / max(2, 1)
	return [
        {
            "provider": "mock_hotels",
            "name": "Sample Inn",
            "price_per_day": avg_night_budget * 0.6,
            "rating": 4.2,
        },
        {
            "provider": "mock_hotels",
            "name": "Demo Hotel",
            "price_per_day": avg_night_budget * 0.8,
            "rating": 4.6,
        },
    ]
