def search_flights():
    return [
        {
            "provider": "mock_flights", 
            "airline": "Mock Air", 
            "price": 3 * 0.4, 
            "duration_hours": 10
        },
        {
            "provider": "mock_flights", 
            "airline": "Sample Airlines", 
            "price": 3 * 0.5, 
            "duration_hours": 12
        },
    ]