/**
 * UI module — renders weather and nearby alternatives in the sidebar.
 */
import { fetchWeather, fetchPrediction } from "./apiClient.js";

/**
 * Load and display weather in the sidebar (US4).
 */
export async function loadWeather() {
    const panel = document.getElementById("weather-panel");
    try {
        const weather = await fetchWeather();
        if (!weather || weather.length === 0) {
            panel.querySelector("p").textContent = "No weather data available.";
            return;
        }

        const w = weather[0];
        const iconUrl = `https://openweathermap.org/img/wn/${w.icon}@2x.png`;

        panel.innerHTML = `
            <h2>Weather</h2>
            <div class="weather-info">
                <img src="${iconUrl}" alt="${w.description}" width="48" height="48"
                     onerror="this.style.display='none'">
                <div>
                    <div class="weather-temp">${Math.round(w.temp)}°C</div>
                    <div>${w.description}</div>
                </div>
            </div>
        `;
    } catch (err) {
        console.error("Weather load error:", err);
        panel.querySelector("p").textContent = "Weather unavailable.";
    }
}

export async function loadPrediction(stationId, date, time) {
    const resultBox = document.getElementById("prediction-result");

    if (!resultBox) return;

    if (!stationId || !date || !time) {
        resultBox.innerHTML = `<p class="placeholder-text">Please enter station ID, date, and time.</p>`;
        return;
    }

    resultBox.innerHTML = `<p class="placeholder-text">Loading prediction...</p>`;

    try {
        const data = await fetchPrediction(stationId, date, time);

        const statusClass =
            data.availability_status === "Likely available"
                ? "status-good"
                : "status-bad";

        resultBox.innerHTML = `
            
            <p><strong>Predicted Bikes:</strong> ${data.predicted_bikes}</p>
            <p><strong>Status:</strong> <span class="${statusClass}">${data.availability_status}</span></p>
            <p>${data.message}</p>
        `;
    } catch (err) {
        console.error("Prediction load error:", err);
        resultBox.innerHTML = `<p class="placeholder-text">Prediction unavailable.</p>`;
    }
}

export function setPredictionStation(stationId, stationName) {
    const stationIdInput = document.getElementById("predict-station-id");
    const stationNameInput = document.getElementById("predict-station-name");

    if (stationIdInput) {
        stationIdInput.value = stationId;
    }

    if (stationNameInput) {
        stationNameInput.value = stationName;
    }
} 

/**
 * Show nearby stations with bikes/stands available (US5).
 * @param {object} selectedStation - the station the user clicked
 * @param {Array}  allStations     - all 117 stations
 * @param {object} availability    - latest availability for selectedStation
 */
export function showNearbyAlternatives(selectedStation, allStations, availability) {
    const panel = document.getElementById("nearby-panel");
    const list  = document.getElementById("nearby-list");

    const needBike  = availability.available_bikes === 0;
    const needStand = availability.available_bike_stands === 0;

    // Only show panel when the selected station is empty or full
    if (!needBike && !needStand) {
        panel.style.display = "none";
        return;
    }

    // Calculate distance (km) from selected station to each other station
    const withDistance = allStations
        .filter(s => s.number !== selectedStation.number)
        .map(s => ({
            ...s,
            distance: haversine(
                selectedStation.latitude, selectedStation.longitude,
                s.latitude, s.longitude
            ),
        }))
        .sort((a, b) => a.distance - b.distance)
        .slice(0, 10); // check the 10 nearest

    // We don't have real-time availability for all stations here,
    // so show the 5 nearest as "check nearby" suggestions
    const label = needBike ? "bikes" : "free stands";
    panel.style.display = "block";
    list.innerHTML = withDistance.slice(0, 5).map(s => `
        <li>
            <strong>${s.name}</strong><br>
            <span style="color:#666; font-size:0.8rem">
                ${(s.distance * 1000).toFixed(0)} m away
            </span>
            <span class="nearby-availability"> — check for ${label}</span>
        </li>
    `).join("");
}

/**
 * Haversine formula — distance in km between two lat/lng points.
 */
function haversine(lat1, lng1, lat2, lng2) {
    const R = 6371;
    const dLat = toRad(lat2 - lat1);
    const dLng = toRad(lng2 - lng1);
    const a = Math.sin(dLat / 2) ** 2
            + Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLng / 2) ** 2;
    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

function toRad(deg) { return deg * Math.PI / 180; }
