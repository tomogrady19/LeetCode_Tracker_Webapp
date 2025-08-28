let chart = null;

async function fetchStats() {
    const username = document.getElementById("username").value.trim();
    const loading = document.getElementById("loading");
    const error = document.getElementById("error");
    const stats = document.getElementById("stats");

    if (!username) {
        showError("Please enter a username");
        return;
    }

    loading.classList.remove("hidden");
    error.classList.add("hidden");
    stats.classList.add("hidden");

    try {
        const response = await fetch(`/api/stats/${encodeURIComponent(username)}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong");
        }

        displayStats(data);
    } catch (err) {
        showError(err.message);
    } finally {
        loading.classList.add("hidden");
    }
}

function showError(message) {
    const error = document.getElementById("error");
    error.textContent = message;
    error.classList.remove("hidden");
}

function displayStats(data) {
    document.getElementById("userDisplay").textContent = `Stats for ${data.username}`;
    document.getElementById("easy").textContent = data.easy;
    document.getElementById("medium").textContent = data.medium;
    document.getElementById("hard").textContent = data.hard;
    document.getElementById("total").textContent = data.total;

    document.getElementById("stats").classList.remove("hidden");
    drawChart(data);
}

function drawChart(data) {
    const ctx = document.getElementById("chart").getContext("2d");

    if (chart) {
        chart.destroy();
    }

    chart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: ["Easy", "Medium", "Hard"],
            datasets: [{
                label: "Problems Solved",
                data: [data.easy, data.medium, data.hard],
                backgroundColor: ["#4caf50", "#ff9800", "#f44336"]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                title: {
                    display: true,
                    text: "Problems Solved by Difficulty"
                }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}