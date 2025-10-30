let currentCity = "";
let currentWeather = {};

document.getElementById("weatherForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const city = e.target.city.value;
  currentCity = city;

  const res = await fetch("/weather", {
    method: "POST",
    body: new URLSearchParams({ city }),
  });

  if (!res.ok) {
    document.getElementById("weatherResult").innerHTML =
      "<p style='color:red;'>Error fetching weather data.</p>";
    return;
  }

  const data = await res.json();
  currentWeather = data;

  document.getElementById("weatherResult").innerHTML = `
    <h3>${data.city}</h3>
    <p>🌡️ ${data.temp}°C</p>
    <p>${data.description}</p>
    <p>💧 Humidity: ${data.humidity}%</p>
    <p><strong>🤖 AI Summary:</strong> ${data.ai_summary}</p>
  `;

  // Initialize Map
  initMap(data.city);
});

document.getElementById("askAI").addEventListener("click", async () => {
  const prompt = document.getElementById("prompt").value;
  const responseEl = document.getElementById("aiResponse");

  if (!prompt) {
    responseEl.innerText = "Please type a question!";
    return;
  }

  // Include weather data in AI prompt
  const payload = {
    prompt: `${prompt}\n\nCity: ${currentWeather.city}\nTemp: ${currentWeather.temp}°C\nCondition: ${currentWeather.description}`,
  };

  try {
    const res = await fetch("/assistant_ai", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    // ❗Fix: Avoid parsing HTML error as JSON
    const text = await res.text();
    try {
      const json = JSON.parse(text);
      responseEl.innerText = json.response || "No response from AI.";
    } catch {
      responseEl.innerHTML =
        "<span style='color:red;'>Server error — check backend console.</span>";
      console.error("Invalid JSON:", text);
    }
  } catch (error) {
    responseEl.innerText = "⚠️ AI request failed.";
  }
});

function initMap(city) {
  fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${city}`)
    .then((res) => res.json())
    .then((data) => {
      if (data.length === 0) return;
      const { lat, lon } = data[0];
      const map = L.map("map").setView([lat, lon], 10);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors",
      }).addTo(map);
      L.marker([lat, lon]).addTo(map).bindPopup(city).openPopup();
    });
}