# Weather DevOps App (Beginner → Intermediate)
This project is a small **Weather Forecast** web app (Flask) that uses the **OpenWeather API**.
It is setup to demonstrate **5 DevOps tools**: Git/GitHub, Docker, Jenkins, Prometheus, Grafana.
It is Mac M4 compatible.

## Files included
- app.py
- templates/index.html
- Dockerfile
- requirements.txt
- Jenkinsfile
- prometheus.yml

## API Key
- The project will use the OpenWeather API key.
- You provided a key in the setup, which is embedded as a fallback in `app.py`.
- Safer option: set it as an environment variable before running:
  ```bash
  export OPENWEATHER_API_KEY=your_real_api_key_here
  ```

## Quick start (Mac M4)

1. Open Terminal and go to project folder:
   ```bash
   cd ~/path/to/weather-devops
   ```

2. Build Docker image (recommended for Apple Silicon):
   ```bash
   docker buildx build --platform linux/arm64 -t weather-devops-app --load .
   ```

3. Run container:
   ```bash
   docker run -d --name weather-devops-run -p 5000:5000 weather-devops-app
   ```

4. Open in browser:
   http://localhost:5000

## Prometheus (monitoring)
1. Run Prometheus (reads `prometheus.yml` in this folder):
   ```bash
   docker run -d -p 9090:9090 -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml --name prometheus prom/prometheus
   ```
2. Prometheus UI: http://localhost:9090

## Grafana (visualization)
   ```bash
   docker run -d -p 3000:3000 --name grafana grafana/grafana
   ```
   Open http://localhost:3000 (login admin/admin)
   Add Prometheus as data source: `http://host.docker.internal:9090`

## Jenkins (CI/CD)
- Optionally run Jenkins in Docker:
   ```bash
   docker run -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts
   ```
- Create a Pipeline job and point to this repo (or local files). The included `Jenkinsfile` will build and run Docker image.

## Notes
- For production use, DO NOT embed API keys in code. Use environment variables or secret managers.
- If Docker images fail on Apple Silicon, ensure Docker Desktop is up to date and use `docker buildx` command shown above.
