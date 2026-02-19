async function loadDashboard() {

    const client = "YourClientName";

    const res = await fetch(`/analytics/${client}`);

    document.getElementById("total").innerText = data.total;

    document.getElementById("hot").innerText = data.hot;

    document.getElementById("warm").innerText = data.warm;

    document.getElementById("cold").innerText = data.cold
}

loadDashboard();