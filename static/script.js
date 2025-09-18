let map, userMarker, routingControl, userLocation;

function initMap() {
  map = L.map('map').setView([20.5937, 78.9629], 5); // India center

  L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/">OSM</a> contributors',
    subdomains: 'abcd',
    maxZoom: 20
  }).addTo(map);

  // Get user location
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(pos => {
      const lat = pos.coords.latitude;
      const lng = pos.coords.longitude;
      userLocation = [lat, lng];
      map.setView(userLocation, 14);
      userMarker = L.marker(userLocation, { icon: blueMarker() })
        .addTo(map)
        .bindPopup("You are here")
        .openPopup();
    }, () => { alert("Location access denied."); });
  }
}

function blueMarker() {
  return L.icon({
    iconUrl: "https://cdn-icons-png.flaticon.com/512/684/684908.png",
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -28]
  });
}

function redMarker() {
  return L.icon({
    iconUrl: "https://cdn-icons-png.flaticon.com/512/2967/2967350.png",
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -28]
  });
}

function findHospitals() {
  if (!userLocation) { alert("Location not available."); return; }
  const [lat, lng] = userLocation;
  const overpassUrl = `https://overpass-api.de/api/interpreter?data=[out:json];node(around:5000,${lat},${lng})[amenity=hospital];out;`;

  fetch(overpassUrl)
    .then(res => res.json())
    .then(data => {
      if (data.elements.length === 0) { alert("No hospitals nearby."); return; }
      data.elements.forEach(el => {
        if (el.lat && el.lon) {
          const marker = L.marker([el.lat, el.lon], { icon: redMarker() }).addTo(map);
          marker.bindPopup(el.tags.name || "Hospital").on("click", () => {
            if (routingControl) map.removeControl(routingControl);
            routingControl = L.Routing.control({
              waypoints: [ L.latLng(lat, lng), L.latLng(el.lat, el.lon) ],
              lineOptions: { styles: [{ color: '#007bff', weight: 5 }] },
              createMarker: () => null,
              routeWhileDragging: false
            }).addTo(map);
          });
        }
      });
    });
}

// ---------- Chat UX ----------
function userBubble(text) {
  return `<div class="user-msg">${escapeHtml(text)}</div>`;
}

function botBubbleHtml(html) {
  return `<div class="bot-msg">${html}</div>`;
}

function escapeHtml(unsafe) {
  return unsafe
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function renderResultCard(res) {
  const confVal = parseInt((res.confidence || "0%").replace("%", ""), 10);
  const specialist = res.specialist || "";
  const aliases = res.aliases || "N/A";

  return `
  <div class="result-card card mb-2 shadow-sm">
    <div class="card-body p-2">
      <div class="d-flex align-items-center">
        <div class="mr-2">
          <i class="fa fa-notes-medical fa-2x text-primary"></i>
        </div>
        <div class="w-100">
          <div class="d-flex justify-content-between">
            <h5 class="card-title mb-1">${escapeHtml(res.disease)}</h5>
            <small class="text-muted">${escapeHtml(aliases)}</small>
          </div>
          <div class="mb-1"><small class="text-muted">Specialist: ${escapeHtml(specialist)}</small></div>

          <div class="mb-1">
            <div class="progress" style="height:16px;">
              <div class="progress-bar" role="progressbar" style="width:${confVal}%" aria-valuenow="${confVal}" aria-valuemin="0" aria-valuemax="100">
                ${confVal}%
              </div>
            </div>
          </div>

          <div class="small text-muted mb-1"><b>Symptoms:</b> ${escapeHtml(res.symptoms)}</div>
          <div class="small text-muted mb-1"><b>Medicines:</b> ${escapeHtml(res.medicines)}</div>
          <div class="small text-muted mb-1"><b>Precautions:</b> ${escapeHtml(res.precautions)}</div>

          <div class="mt-2 d-flex gap-2">
            <button class="btn btn-sm btn-outline-primary more-info" data-query="${encodeURIComponent(res.disease + ' symptoms')}">More info</button>
            <button class="btn btn-sm btn-outline-secondary copy" data-text="${escapeHtml(res.disease)}">Copy</button>
          </div>
        </div>
      </div>
    </div>
  </div>
  `;
}

// Send message
function sendMessage(msg) {
  if (!msg || !msg.trim()) return;
  $("#chat-container").append(userBubble(msg));
  $("#chat-container").scrollTop($("#chat-container")[0].scrollHeight);
  $("#user-input").val("");

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: msg })
  })
  .then(res => res.json())
  .then(data => {
    if (data.results) {
      if (data.reply) {
        // show web fallback above results if present
        $("#chat-container").append(botBubbleHtml(data.reply));
      }
      data.results.forEach(r => {
        $("#chat-container").append(renderResultCard(r));
      });
    } else if (data.reply) {
      // If reply includes raw HTML (links), inject safely
      $("#chat-container").append(botBubbleHtml(data.reply));
    }
    $("#chat-container").scrollTop($("#chat-container")[0].scrollHeight);
  })
  .catch(err => {
    console.error(err);
    $("#chat-container").append(botBubbleHtml("Sorry, something went wrong. Try again."));
    $("#chat-container").scrollTop($("#chat-container")[0].scrollHeight);
  });
}

$(document).ready(function() {
  // send on click
  $("#send-btn").on("click", () => {
    const val = $("#user-input").val().trim();
    sendMessage(val);
  });

  // quick symptom buttons
  $(document).on("click", ".quick-symptom", function() {
    const s = $(this).text();
    $("#user-input").val((prev => (prev ? prev + ", " + s : s))($("#user-input").val()));
  });

  // more-info and copy handlers (delegated)
  $(document).on("click", ".more-info", function() {
    const q = $(this).data("query");
    window.open("https://www.google.com/search?q=" + q, "_blank");
  });
  $(document).on("click", ".copy", function() {
    const text = $(this).data("text");
    navigator.clipboard && navigator.clipboard.writeText(text);
    $(this).text("Copied");
    setTimeout(() => $(this).text("Copy"), 1200);
  });

  // clear chat
  $("#clear-chat").on("click", () => {
    $("#chat-container").empty();
  });

  // enter key sends
  $("#user-input").on("keypress", function(e) {
    if (e.which === 13) {
      e.preventDefault();
      $("#send-btn").click();
    }
  });

  // nearby hospitals button
  $("#find-hospitals-btn").on("click", () => { findHospitals(); });

  initMap();
});
