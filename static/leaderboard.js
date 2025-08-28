async function loadLeaderboard() {
    const loading = document.getElementById("loading");
    const error = document.getElementById("error");
    const leaderboard = document.getElementById("leaderboard");
    const emptyLeaderboard = document.getElementById("empty-leaderboard");

    loading.classList.remove("hidden");
    error.classList.add("hidden");
    leaderboard.classList.add("hidden");
    emptyLeaderboard.classList.add("hidden");

    try {
        const response = await fetch("/api/leaderboard");
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Failed to load leaderboard");
        }

        displayLeaderboard(data.entries);
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

function displayLeaderboard(entries) {
    const leaderboard = document.getElementById("leaderboard");
    const emptyLeaderboard = document.getElementById("empty-leaderboard");
    const tbody = document.getElementById("leaderboard-body");

    if (entries.length === 0) {
        emptyLeaderboard.classList.remove("hidden");
        return;
    }

    tbody.innerHTML = "";
    entries.forEach((entry, index) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td class="rank">${index + 1}</td>
            <td class="username">${entry.username}</td>
            <td class="checks">${entry.check_count}</td>
            <td class="total-solved">${entry.total_solved}</td>
        `;
        tbody.appendChild(row);
    });

    leaderboard.classList.remove("hidden");
}

// Load leaderboard when page loads
document.addEventListener("DOMContentLoaded", loadLeaderboard);