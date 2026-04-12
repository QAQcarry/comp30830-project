/**
 * API client module — fetch wrappers for Flask backend endpoints.
 */

function handleUnauthorized(response) {
    if (response.status === 401 || response.redirected) {
        window.location.href = "/auth/login";
        throw new Error("Session expired. Redirecting to login.");
    }
}

export async function fetchStations() {
    const response = await fetch("/stations");
    handleUnauthorized(response);
    if (!response.ok) throw new Error("Failed to fetch stations");
    const data = await response.json();
    return data.stations;
}

export async function fetchAvailability(stationId) {
    const response = await fetch(`/available/${stationId}`);
    handleUnauthorized(response);
    if (!response.ok) throw new Error(`Failed to fetch availability for station ${stationId}`);
    const data = await response.json();
    return data.availability;
}

export async function fetchAllAvailability() {
    const response = await fetch("/available/all");
    handleUnauthorized(response);
    if (!response.ok) throw new Error("Failed to fetch all availability");
    const data = await response.json();
    return data.availability;
}

export async function fetchAvailabilityHistory(stationId) {
    const response = await fetch(`/available/${stationId}/history`);
    handleUnauthorized(response);
    if (!response.ok) throw new Error(`Failed to fetch history for station ${stationId}`);
    const data = await response.json();
    return data.history;
}

export async function fetchWeather() {
    const response = await fetch("/weather");
    handleUnauthorized(response);
    if (!response.ok) throw new Error("Failed to fetch weather");
    const data = await response.json();
    return data.weather;
}

export async function fetchPrediction(stationId, date, time) {
    const response = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            station_id: parseInt(stationId, 10),
            date: date,
            time: time
        })
    });

    handleUnauthorized(response);

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.message || "Failed to fetch prediction");
    }

    return data;
}