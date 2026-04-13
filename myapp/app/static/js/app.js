/**
 * App entry point — initializes map and sets up event listeners.
 */
import { initMap, filterStations } from "./mapManager.js";
import { loadWeather } from "./ui.js";
import { loadWeather, loadPrediction } from "./ui.js";

// Expose initMap to global scope for Google Maps callback
window.initMap = initMap;

async function requestPrediction() {
    const stationInput = document.getElementById("predict-station-id");
    const dateInput = document.getElementById("predict-date");
    const timeInput = document.getElementById("predict-time");
    const resultBox = document.getElementById("prediction-result");

    if (!stationInput || !dateInput || !timeInput || !resultBox) {
        return;
    }

    const stationId = stationInput.value.trim();
    const date = dateInput.value;
    const time = timeInput.value;

    if (!stationId || !date || !time) {
        resultBox.innerHTML = `<p class="placeholder-text">Please enter station ID, date, and time.</p>`;
        return;
    }

    resultBox.innerHTML = `<p class="placeholder-text">Loading prediction...</p>`;

    try {
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

        const data = await response.json();

        if (!response.ok) {
            resultBox.innerHTML = `<p class="placeholder-text">${data.message || "Prediction failed."}</p>`;
            return;
        }

        const statusClass =
            data.availability_status === "Likely available"
                ? "status-good"
                : "status-bad";

        resultBox.innerHTML = `
            <p><strong>Station:</strong> ${data.station_id}</p>
            <p><strong>Predicted Bikes:</strong> ${data.predicted_bikes}</p>
            <p><strong>Status:</strong> <span class="${statusClass}">${data.availability_status}</span></p>
            <p>${data.message}</p>
        `;
    } catch (error) {
        console.error("Prediction request failed:", error);
        resultBox.innerHTML = `<p class="placeholder-text">Unable to fetch prediction right now.</p>`;
    }
}

// Set up event listeners once DOM is ready
document.addEventListener("DOMContentLoaded", () => {
    loadWeather();

    const searchInput = document.getElementById("station-search");
    if (searchInput) {
        searchInput.addEventListener("input", (e) => {
            filterStations(e.target.value);
        });
    }

    const predictBtn = document.getElementById("predict-btn");
    if (predictBtn) {
        predictBtn.addEventListener("click", () => {
            const stationId = document.getElementById("predict-station-id")?.value.trim();
            const date = document.getElementById("predict-date")?.value;
            const time = document.getElementById("predict-time")?.value;

        loadPrediction(stationId, date, time);
        });
    }   
});

