function getClientFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("client");

}

async function loadDashboard() {
    const client = getClientFromURL();

    if (!client) {
        alert("Client name missing in URL")
        return;
    }

    const res = await fetch(`/analytics/${client}`);
    const data = await res.json();

    document.getElementById("total").innerText = data.total;

    document.getElementById("hot").innerText = data.hot;

    document.getElementById("warm").innerText = data.warm;
    
    document.getElementById("cold").innerText = data.cold;
}

loadDashboard();