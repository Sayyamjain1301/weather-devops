<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🌤️ Smart Weather Dashboard</title>

  <style>
    body {
      margin: 0;
      font-family: 'Poppins', sans-serif;
      color: white;
      background: linear-gradient(to bottom right, #00c6ff, #0072ff);
      overflow-x: hidden;
    }

    /* 🌥️ Animated Clouds */
    .clouds {
      position: absolute;
      top: 0;
      left: 0;
      width: 300%;
      height: 200px;
      background: url('https://png.pngtree.com/thumb_back/fw800/background/20231006/pngtree-soft-clouds-background-image_13529122.png') repeat-x;
      background-size: contain;
      animation: moveClouds 60s linear infinite;
      opacity: 0.3;
      z-index: 1;
    }

    @keyframes moveClouds {
      from { transform: translateX(0); }
      to { transform: translateX(-50%); }
    }

    /* 🌤️ Center container */
    .container {
      position: relative;
      z-index: 2;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      text-align: center;
      padding: 20px;
    }

    h1 {
      font-size: 2.5rem;
      font-weight: 700;
      margin-bottom: 0.5rem;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    p {
      font-size: 1.1rem;
      opacity: 0.8;
      margin-bottom: 1.5rem;
    }

    input[type="text"] {
      padding: 12px 20px;
      width: 260px;
      border: none;
      border-radius: 30px;
      outline: none;
      text-align: center;
      font-size: 1rem;
      box-shadow: 0 0 10px rgba(255,255,255,0.3);
    }

    button {
      padding: 12px 20px;
      background: white;
      color: #0072ff;
      border: none;
      border-radius: 30px;
      margin-left: 10px;
      cursor: pointer;
      font-weight: bold;
      transition: 0.3s;
    }

    button:hover {
      background: #0072ff;
      color: white;
      transform: scale(1.05);
    }

    .result {
      margin-top: 30px;
      padding: 20px;
      background: rgba(255,255,255,0.15);
      border-radius: 15px;
      backdrop-filter: blur(6px);
      box-shadow: 0 4px 15px rgba(0,0,0,0.3);
      display: inline-block;
      animation: fadeIn 1s ease-in-out;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .footer {
      position: absolute;
      bottom: 10px;
      font-size: 0.9rem;
      opacity: 0.8;
    }

    /* 📱 Responsive */
    @media (max-width: 600px) {
      h1 { font-size: 1.8rem; }
      input[type="text"] { width: 200px; }
    }
  </style>
</head>

<body>
  <div class="clouds"></div>

  <div class="container">
    <h1>🌦️ Smart Weather Dashboard</h1>
    <p>Check live weather, humidity, and wind speed</p>

    <form method="POST">
      <input type="text" name="city" placeholder="Enter City Name" required>
      <button type="submit">Search</button>
    </form>

    {% if weather %}
      <div class="result">
        <h2>🌍 {{ weather['city'] }}</h2>
        <p>🌡️ Temperature: {{ weather['temperature'] }}°C</p>
        <p>💧 Humidity: {{ weather['humidity'] }}%</p>
        <p>🌬️ Wind Speed: {{ weather['wind_speed'] }} m/s</p>
        <p>☁️ Condition: {{ weather['description'] }}</p>
      </div>
    {% endif %}

    <div class="footer">
      ☁️ Developed by <b>Sayyam Jain</b> | Flask + DevOps + Cloud ☁️
    </div>
  </div>
</body>
</html>