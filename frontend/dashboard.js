function getClientFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get("client");
}

async function loadDashboard() {
  showLoader();
  const client = getClientFromURL();

  if (!client) {
    hideLoader();
    alert("Client name missing in URL");
    return;
  }

  const res = await fetch(`/analytics/${client}`);
  const data = await res.json();

  animateValue("total", data.total);
  animateValue("hot", data.hot);
  animateValue("warm", data.warm);
  animateValue("cold", data.cold);

  createChart(data);
  await loadLeadsTable(client);

  hideLoader();
}

function createChart(data) {
  const ctx = document.getElementById("leadChart").getContext("2d");

  new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: ["Hot", "Warm", "Cold"],
      datasets: [{
        data: [data.hot, data.warm, data.cold],
        backgroundColor: [
          "rgba(239, 68, 68, 0.8)",
          "rgba(234, 179, 8, 0.8)",
          "rgba(59, 130, 246, 0.8)"
        ],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          labels: {
            color: "white",
            font: { size: 14 }
          }
        }
      }
    }
  });

}

async function loadLeadsTable(client) {
  const res = await fetch(`/leads/${client}`);
  const leads = await res.json();
  allLeads = leads || [];
  renderTable();
  
}
let allLeads = [];
let currentFilter = "all";

function setFilter(status) {
  currentFilter = status;
  renderTable();
}

document.getElementById("searchInput").addEventListener("input", renderTable);

function renderTable() {
  const searchValue = document.getElementById("searchInput").value.toLowerCase();

  const filtered = allLeads.filter(lead => {

    const matchesSearch =
      lead.name?.toLowerCase().includes(searchValue) ||
      lead.email?.toLowerCase().includes(searchValue);

    const matchesStatus =
      currentFilter === "all" || lead.status === currentFilter;

    return matchesSearch && matchesStatus;
  });

  const table = document.getElementById("leadsTable");
  table.innerHTML = "";

  filtered.forEach(lead => {
    table.innerHTML += `
      <tr>
        <td class="py-3 px-4">${lead.id}</td>
        <td class="py-3 px-4">${lead.name}</td>
        <td class="py-3 px-4">${lead.email}</td>
        <td class="py-3 px-4">${lead.company}</td>
        <td class="py-3 px-4">$${lead.budget}</td>
        <td class="py-3 px-4">${lead.score}</td>
        <td class="py-3 px-4">${getStatusBadge(lead.status)}</td>
        <td class="py-3 px-4">${new Date(lead.created_at).toLocaleDateString()}</td>
      </tr>
    `;
  });
}
function getStatusBadge(status) {
  const base = "px-3 py-1 rounded-full text-xs font-semibold";

  if (status === "hot") {
    return `<span class="${base} bg-red-600 text-white">HOT</span>`;
  }
  if (status === "warm") {
    return `<span class="${base} bg-yellow-500 text-black">WARM</span>`;
  }
  if (status === "cold") {
    return `<span class="${base} bg-blue-600 text-white">COLD</span>`;
  }

  return `<span class="${base} bg-gray-600 text-white">${status}</span>`;
}

function animateValue(id, end) {
  let start = 0;
  const duration = 800;
  const stepTime = Math.abs(Math.floor(duration / end || 1));

  const obj = document.getElementById(id);
  const timer = setInterval(() => {
    start++;
    obj.innerText = start;
    if (start >= end) clearInterval(timer);
  }, stepTime);
}
function exportLeads() {
  const client = getClientFromURL();
  window.open(`/export/${client}`, "_blank");
}
function showLoader() {
  document.getElementById("loader").classList.remove("hidden");
}

function hideLoader() {
  document.getElementById("loader").classList.add("hidden");
}

loadDashboard();
