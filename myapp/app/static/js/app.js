/**
 * App entry point — initializes map and sets up event listeners.
 */
import { initMap, filterStations } from "./mapManager.js";
import { loadWeather } from "./ui.js";

// Expose initMap to global scope for Google Maps callback
window.initMap = initMap;

// Set up event listeners once DOM is ready
document.addEventListener("DOMContentLoaded", () => {
    loadWeather();

    const searchInput = document.getElementById("station-search");
    if (searchInput) {
        searchInput.addEventListener("input", (e) => {
            filterStations(e.target.value);
        });
    }
});
