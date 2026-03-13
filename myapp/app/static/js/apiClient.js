/**
 * API client module — fetch wrappers for Flask backend endpoints.
 */

export async function fetchStations() {
    const response = await fetch("/stations");
    if (!response.ok) throw new Error("Failed to fetch stations");
    const data = await response.json();
    return data.stations;
}

export async function fetchAvailability(stationId) {
    const response = await fetch(`/available/${stationId}`);
    if (!response.ok) throw new Error(`Failed to fetch availability for station ${stationId}`);
    const data = await response.json();
    return data.availability;
}

export async function fetchAllAvailability() {
    const response = await fetch("/available/all");
    if (!response.ok) throw new Error("Failed to fetch all availability");
    const data = await response.json();
    return data.availability;
}

export async function fetchAvailabilityHistory(stationId) {
    const response = await fetch(`/available/${stationId}/history`);
    if (!response.ok) throw new Error(`Failed to fetch history for station ${stationId}`);
    const data = await response.json();
    return data.history;
}

export async function fetchWeather() {
    const response = await fetch("/weather");
    if (!response.ok) throw new Error("Failed to fetch weather");
    const data = await response.json();
    return data.weather;
}
