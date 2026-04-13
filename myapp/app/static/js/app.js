/**
 * App entry point — initializes map and sets up event listeners.
 */
import { initMap, filterStations, getStations, selectStationByNumber } from "./mapManager.js";
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
    const searchResults = document.getElementById("search-results");

    function renderSearchResults(query) {
        if (!searchResults) return;
        const q = query.trim().toLowerCase();
        if (!q) {
            searchResults.hidden = true;
            searchResults.innerHTML = "";
            return;
        }
        const matches = getStations()
            .filter(s => s.name.toLowerCase().includes(q))
            .slice(0, 8);
        if (matches.length === 0) {
            searchResults.innerHTML = `<li class="search-empty">No stations match "${query}"</li>`;
            searchResults.hidden = false;
            return;
        }
        searchResults.innerHTML = matches.map(s => `
            <li data-station-number="${s.number}">
                <strong>${s.name}</strong>
                ${s.address ? `<span class="search-meta">${s.address}</span>` : ""}
            </li>
        `).join("");
        searchResults.hidden = false;
    }

    if (searchInput) {
        searchInput.addEventListener("input", (e) => {
            filterStations(e.target.value);
            renderSearchResults(e.target.value);
        });
        searchInput.addEventListener("focus", (e) => {
            if (e.target.value.trim()) renderSearchResults(e.target.value);
        });
    }

    if (searchResults) {
        searchResults.addEventListener("mousedown", (e) => {
            const li = e.target.closest("li[data-station-number]");
            if (!li) return;
            e.preventDefault();
            const number = parseInt(li.dataset.stationNumber, 10);
            selectStationByNumber(number);
            searchInput.value = li.querySelector("strong").textContent;
            filterStations("");
            searchResults.hidden = true;
        });
    }

    document.addEventListener("click", (e) => {
        if (!searchResults) return;
        if (!e.target.closest(".search-wrapper")) {
            searchResults.hidden = true;
        }
    });

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

