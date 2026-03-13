/**
 * Chart module — draws availability history using Google Charts.
 */
import { fetchAvailabilityHistory } from "./apiClient.js";

let chartsLoaded = false;

// Load Google Charts package once
google.charts.load("current", { packages: ["corechart"] });
google.charts.setOnLoadCallback(() => { chartsLoaded = true; });

/**
 * Draw availability history chart for a station.
 * @param {number} stationId - the station number
 */
export async function drawAvailabilityChart(stationId) {
    const container = document.getElementById("chart-container");
    container.innerHTML = '<p class="loading">Loading chart...</p>';

    // Wait for Google Charts to be ready
    if (!chartsLoaded) {
        await new Promise(resolve => {
            google.charts.setOnLoadCallback(resolve);
        });
    }

    try {
        const history = await fetchAvailabilityHistory(stationId);

        if (!history || history.length === 0) {
            container.innerHTML = '<p class="loading">No history data available.</p>';
            return;
        }

        // Build DataTable
        const dataTable = new google.visualization.DataTable();
        dataTable.addColumn("datetime", "Time");
        dataTable.addColumn("number", "Available Bikes");
        dataTable.addColumn("number", "Free Stands");

        for (const row of history) {
            // last_update is a Unix timestamp in milliseconds (bigint from JCDecaux)
            const time = new Date(row.last_update);
            dataTable.addRow([time, row.available_bikes, row.available_bike_stands]);
        }

        const options = {
            title: "Availability (Last 24h)",
            curveType: "function",
            legend: { position: "bottom" },
            height: 250,
            colors: ["#2e7d32", "#1565c0"],
            hAxis: {
                title: "Time",
                format: "HH:mm",
            },
            vAxis: {
                title: "Count",
                minValue: 0,
            },
            chartArea: { width: "80%", height: "60%" },
        };

        container.innerHTML = "";
        const chart = new google.visualization.LineChart(container);
        chart.draw(dataTable, options);

    } catch (err) {
        console.error("Chart error:", err);
        container.innerHTML = '<p class="loading">Chart unavailable.</p>';
    }
}
