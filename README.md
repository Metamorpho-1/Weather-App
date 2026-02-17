#  Global Ecosystem Intelligence (Weather Dashboard)

Hey there! Welcome to my Python desktop weather application.

I built this project to deepen my understanding of desktop GUI frameworks (PyQt5) and RESTful API integration. While many beginner weather apps simply freeze the terminal or the UI while waiting for internet data, I specifically designed this dashboard to remain fluid and responsive by handling network operations asynchronously. 

## Core Features

* **Zero-Config API Integration:** I transitioned the app from OpenWeatherMap to the **Open-Meteo API**. This means you can clone this repo and run it instantly without having to sign up for an API key. It utilizes a two-step process: geocoding the city to coordinates, then fetching the highly detailed weather data.
* **Asynchronous QThreading:** The network requests are offloaded to a background `QThread`. This ensures the main application window never freezes or says "(Not Responding)" while waiting for the server to reply. 
* **Sleek, Modern UI:** Designed with a "Neural" dark mode theme, featuring deep slate backgrounds, rounded inputs, and emerald green accents powered by PyQt Style Sheets (QSS).
* **Universal Font & Emoji Handling:** The CSS is specifically tuned with a universal font stack so it renders native Apple UI fonts and full-color emojis on macOS, while gracefully degrading to Segoe UI on Windows.
* **WMO Standardized Parsing:** Instead of guessing weather ranges, the app uses standard World Meteorological Organization (WMO) codes to generate highly accurate descriptions and emoji pairings.

## 🚀 How to Run It Locally

### Prerequisites
You will need Python installed on your machine, along with the `PyQt5` and `requests` libraries.

1. Clone this repository to your local machine:
   ```bash
   git clone [https://github.com/YOUR-USERNAME/python-weather-dashboard.git](https://github.com/YOUR-USERNAME/python-weather-dashboard.git)
   cd python-weather-dashboard

2. Install the required libraries:
    ```bash
    pip install PyQt5 requests

3. Run the application:
   ```bash
   python weather_app.py

## How to Use

1.Launch the application.

2.Type any global city into the search bar (e.g., "Tokyo", "London", "Jaipur").

3.Press Enter or click Scan.

4.The background thread will instantly fetch and display the current temperature (°C), "feels like" temperature, humidity, and wind speed.

## What I Learned
Building this application solidified my understanding of:

1.Event-Driven Programming: Using PyQt5 Signals and Slots to safely pass data from background worker threads to the main GUI thread.

2.JSON Parsing: Handling complex nested JSON objects returned from multi-step API calls.

3.Error Handling: Gracefully catching requests.exceptions to provide the user with clear feedback if their internet drops or if they search for a city that doesn't exist.

