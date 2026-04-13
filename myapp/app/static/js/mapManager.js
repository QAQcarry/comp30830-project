/**
 * Map manager module — Google Maps initialization, markers, and info windows.
 */
import { fetchStations, fetchAvailability, fetchAllAvailability } from "./apiClient.js";
import { showNearbyAlternatives, setPredictionStation } from "./ui.js";
import { drawAvailabilityChart } from "./chart.js";

let map = null;
let markers = [];
let allStations = [];

/**
 * Initialize the Google Map centered on Dublin and load station markers.
 */
export function initMap() {
    const dublin = { lat: 53.35014, lng: -6.266155 };

    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: dublin,
    });

    loadStations();
}

/**
 * Fetch all stations from the backend and place markers on the map.
 */
async function loadStations() {
    try {
        allStations = await fetchStations();
        addMarkers(allStations);

        // Color markers based on real-time availability
        const availability = await fetchAllAvailability();
        const availMap = {};
        for (const a of availability) {
            availMap[a.number] = a;
        }
        for (const marker of markers) {
            const a = availMap[marker.stationData.number];
            if (a) marker.setIcon(getMarkerIcon(a));
        }
    } catch (error) {
        console.error("Error loading stations:", error);
    }
}

function getMarkerIcon(availability) {
    const bikes  = availability.available_bikes;
    const stands = availability.available_bike_stands;
    let color;
    if (bikes === 0)        color = "red";     // no bikes — can't borrow
    else if (stands === 0)  color = "yellow";  // bikes available but nowhere to return
    else                    color = "green";   // all good

    return {
        url: `https://maps.google.com/mapfiles/ms/icons/${color}-dot.png`,
        scaledSize: new google.maps.Size(32, 32),
    };
}

/**
 * Create a marker for each station and attach click handlers.
 */
function addMarkers(stations) {
    for (const station of stations) {
        const marker = new google.maps.Marker({
            position: { lat: station.latitude, lng: station.longitude },
            map: map,
            title: station.name,
            icon: {
                url: "https://maps.google.com/mapfiles/kml/shapes/cycling.png",
                scaledSize: new google.maps.Size(32, 32),
            },
        });

        marker.stationData = station;

        marker.addListener("click", () => {
            onMarkerClick(station);
        });

        markers.push(marker);
    }
}

/**
 * Handle marker click — show station info in the sidebar.
 */
async function onMarkerClick(station) {
    setPredictionStation(station.number, station.name);
    const panel = document.getElementById("station-info-panel");
    panel.style.display = "block";
    const emptyState = document.getElementById("station-empty-state");
    if (emptyState) emptyState.style.display = "none";

    document.getElementById("station-name").textContent = station.name;
    document.getElementById("station-address").textContent = station.address || "";

    // Set loading state
    document.getElementById("available-bikes").textContent = "...";
    document.getElementById("available-stands").textContent = "...";
    document.getElementById("station-status").innerHTML = "";

    // Center map on selected station
    map.panTo({ lat: station.latitude, lng: station.longitude });

    try {
        const availability = await fetchAvailability(station.number);
        if (availability.length > 0) {
            const latest = availability[0];
            updateAvailabilityDisplay(latest);
            showNearbyAlternatives(station, allStations, latest);
            drawAvailabilityChart(station.number);
        }
    } catch (error) {
        console.error("Error fetching availability:", error);
        document.getElementById("available-bikes").textContent = "?";
        document.getElementById("available-stands").textContent = "?";
    }
}

/**
 * Update the sidebar availability cards and status badges.
 */
function updateAvailabilityDisplay(data) {
    const bikesEl    = document.getElementById("available-bikes");
    const standsEl   = document.getElementById("available-stands");
    const statusEl   = document.getElementById("station-status");
    const capacityEl = document.getElementById("station-capacity");

    bikesEl.textContent  = data.available_bikes;
    standsEl.textContent = data.available_bike_stands;

    if (data.bike_stands) {
        const occupied = data.bike_stands - data.available_bike_stands;
        capacityEl.textContent =
            `Total docks: ${data.bike_stands}  ·  In use: ${occupied}  ·  Free: ${data.available_bike_stands}`;
    } else {
        capacityEl.textContent = "";
    }

    // Build status badges (US3: can borrow / can return)
    let badges = "";

    if (data.available_bikes > 0) {
        badges += '<span class="status-badge can-borrow">Can Borrow</span> ';
    } else {
        badges += '<span class="status-badge cannot-borrow">No Bikes</span> ';
    }

    if (data.available_bike_stands > 0) {
        badges += '<span class="status-badge can-return">Can Return</span>';
    } else {
        badges += '<span class="status-badge cannot-return">No Stands</span>';
    }

    statusEl.innerHTML = badges;
}

/**
 * Filter markers by search query — show matching, hide others.
 */
export function filterStations(query) {
    const lowerQuery = query.toLowerCase();
    for (const marker of markers) {
        const name = marker.stationData.name.toLowerCase();
        const visible = name.includes(lowerQuery);
        marker.setVisible(visible);
    }
}

/**
 * Get all loaded stations (for use by other modules).
 */
export function getStations() {
    return allStations;
}

/**
 * Select a station programmatically (e.g. from search dropdown).
 */
export function selectStationByNumber(number) {
    const station = allStations.find(s => s.number === number);
    if (!station) return;
    if (map) {
        map.panTo({ lat: station.latitude, lng: station.longitude });
        map.setZoom(16);
    }
    onMarkerClick(station);
}
