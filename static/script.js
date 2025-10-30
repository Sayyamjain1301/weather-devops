document.addEventListener("DOMContentLoaded", () => {
  const weatherDiv = document.getElementById("weather");
  const aiDiv = document.getElementById("ai-response");

  document.getElementById("search").addEventListener("click", async () => {
    const city = document.getElementById("city").value.trim();
    if (!city) {
      weatherDiv.innerHTML = "<p>Please enter a city name 🌍</p>";
      return;
    }

    weatherDiv.innerHTML = "<p>Fetching weather...</p>";

    try {
      const res = await fetch(`/weather?city=${encodeURIComponent(city)}`);
      const data = await res.json();

      if (data.error) {
        weatherDiv.innerHTML = `<p>❌ ${data.error}</p>`;
      } else {
        weatherDiv.innerHTML = `
          <h3>🌤 ${data.city}</h3>
          <p>🌡️ Temperature: ${data.temp}°C</p>
          <p>💧 Humidity: ${data.humidity}%</p>
          <p>🌬 Wind: ${data.wind} m/s</p>
          <p>📝 Condition: ${data.desc}</p>
        `;
      }
    } catch (err) {
      weatherDiv.innerHTML = `<p>⚠️ Error: ${err.message}</p>`;
    }
  });

  document.getElementById("ask").addEventListener("click", async () => {
    const question = document.getElementById("question").value.trim();
    if (!question) {
      aiDiv.innerHTML = "<p>Please enter a question 🤖</p>";
      return;
    }

    aiDiv.innerHTML = "<p>Thinking...</p>";

    try {
      const res = await fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();

      if (data.error) {
        aiDiv.innerHTML = `<p>❌ ${data.error}</p>`;
      } else {
        aiDiv.innerHTML = `<p>💬 ${data.reply}</p>`;
      }
    } catch (err) {
      aiDiv.innerHTML = `<p>⚠️ Error: ${err.message}</p>`;
    }
  });
});