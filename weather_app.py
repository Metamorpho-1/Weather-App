import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

# ---------------------------------------------------------
# Worker Thread: Prevents the UI from freezing during API calls
# ---------------------------------------------------------
class WeatherWorker(QThread):
    success_signal = pyqtSignal(dict)
    error_signal = pyqtSignal(str)

    def __init__(self, city):
        super().__init__()
        self.city = city

    def run(self):
        try:
            # Step 1: Geocoding API (Get Lat/Lon for the city)
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={self.city}&count=1&format=json"
            geo_response = requests.get(geo_url, timeout=5)
            geo_response.raise_for_status()
            geo_data = geo_response.json()

            if "results" not in geo_data:
                self.error_signal.emit(f"City '{self.city}' not found.")
                return

            lat = geo_data["results"][0]["latitude"]
            lon = geo_data["results"][0]["longitude"]
            city_name = geo_data["results"][0]["name"]
            country = geo_data["results"][0].get("country", "")

            # Step 2: Weather API (Celsius & km/h)
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m&temperature_unit=celsius&wind_speed_unit=kmh"
            weather_response = requests.get(weather_url, timeout=5)
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            # Package the data and send it back to the GUI
            result = {
                "location": f"{city_name}, {country}".strip(", "),
                "temp": weather_data["current"]["temperature_2m"],
                "feels_like": weather_data["current"]["apparent_temperature"],
                "humidity": weather_data["current"]["relative_humidity_2m"],
                "wind": weather_data["current"]["wind_speed_10m"],
                "code": weather_data["current"]["weather_code"]
            }
            self.success_signal.emit(result)

        except requests.exceptions.RequestException:
            self.error_signal.emit("Network Error: Please check your connection.")
        except Exception:
            self.error_signal.emit("An unexpected error occurred.")

# ---------------------------------------------------------
# Main GUI Application
# ---------------------------------------------------------
class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Global Ecosystem Intelligence")
        self.resize(450, 600)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 40, 30, 40)
        main_layout.setSpacing(20)

        # --- Search Bar Area ---
        search_layout = QHBoxLayout()
        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText("Enter a city...")
        self.city_input.returnPressed.connect(self.fetch_weather)
        
        self.search_btn = QPushButton("Scan", self)
        self.search_btn.setCursor(Qt.PointingHandCursor)
        self.search_btn.clicked.connect(self.fetch_weather)

        search_layout.addWidget(self.city_input)
        search_layout.addWidget(self.search_btn)

        # --- Weather Display Area ---
        self.location_label = QLabel("Ready for input.", self)
        self.location_label.setAlignment(Qt.AlignCenter)
        self.location_label.setObjectName("location_label")

        self.emoji_label = QLabel("🌍", self)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setObjectName("emoji_label")

        self.temp_label = QLabel("--°C", self)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.temp_label.setObjectName("temp_label")

        self.details_label = QLabel("Awaiting global sync...", self)
        self.details_label.setAlignment(Qt.AlignCenter)
        self.details_label.setObjectName("details_label")
        self.details_label.setWordWrap(True)

        main_layout.addLayout(search_layout)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.location_label)
        main_layout.addWidget(self.emoji_label)
        main_layout.addWidget(self.temp_label)
        main_layout.addWidget(self.details_label)
        main_layout.addStretch()

        self.setLayout(main_layout)
        self.apply_dark_theme()

    def apply_dark_theme(self):
        """Injects CSS styling for a modern, sleek aesthetic."""
        self.setStyleSheet("""
            QWidget {
                background-color: #0F172A;
                color: #FFFFFF;
                /* Universal system font stack to prevent Mac terminal errors */
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            }
            QLineEdit {
                background-color: #1E293B;
                border: 2px solid #334155;
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
                color: #F8FAFC;
            }
            QLineEdit:focus {
                border: 2px solid #10B981; 
            }
            QPushButton {
                background-color: #10B981;
                color: #0F172A;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #34D399;
            }
            QPushButton:pressed {
                background-color: #059669;
            }
            QLabel#location_label {
                font-size: 22px;
                color: #94A3B8;
                font-weight: 600;
            }
            QLabel#emoji_label {
                font-size: 110px;
                /* Forces macOS to use its native color emojis */
                font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif;
            }
            QLabel#temp_label {
                font-size: 85px;
                font-weight: 800;
                color: #10B981; 
                margin-top: -20px;
            }
            QLabel#details_label {
                font-size: 16px;
                color: #CBD5E1;
                line-height: 1.5;
            }
        """)

    def fetch_weather(self):
        city = self.city_input.text().strip()
        if not city:
            return

        self.search_btn.setText("...")
        self.search_btn.setEnabled(False)
        self.location_label.setText("Scanning network...")
        self.temp_label.setText("--°C")
        self.emoji_label.setText("📡")
        self.details_label.setText("")

        self.worker = WeatherWorker(city)
        self.worker.success_signal.connect(self.update_ui)
        self.worker.error_signal.connect(self.show_error)
        self.worker.start()

    def update_ui(self, data):
        self.search_btn.setText("Scan")
        self.search_btn.setEnabled(True)

        self.location_label.setText(data["location"])
        self.temp_label.setText(f"{round(data['temp'])}°C")
        
        emoji, desc = self.parse_wmo_code(data["code"])
        self.emoji_label.setText(emoji)
        
        details = (f"{desc}\n"
                   f"Feels like: {round(data['feels_like'])}°C | "
                   f"Humidity: {data['humidity']}%\n"
                   f"Wind: {data['wind']} km/h")
        self.details_label.setText(details)

    def show_error(self, message):
        self.search_btn.setText("Scan")
        self.search_btn.setEnabled(True)
        self.location_label.setText("Error")
        self.emoji_label.setText("⚠️")
        self.temp_label.setText("")
        self.details_label.setText(message)

    @staticmethod
    def parse_wmo_code(code):
        wmo_mapping = {
            0: ("☀️", "Clear Sky"),
            1: ("🌤️", "Mainly Clear"),
            2: ("⛅", "Partly Cloudy"),
            3: ("☁️", "Overcast"),
            45: ("🌫️", "Fog"),
            48: ("🌫️", "Depositing Rime Fog"),
            51: ("🌧️", "Light Drizzle"),
            53: ("🌧️", "Moderate Drizzle"),
            55: ("🌧️", "Dense Drizzle"),
            61: ("☔", "Slight Rain"),
            63: ("☔", "Moderate Rain"),
            65: ("☔", "Heavy Rain"),
            71: ("❄️", "Slight Snow Fall"),
            73: ("❄️", "Moderate Snow Fall"),
            75: ("❄️", "Heavy Snow Fall"),
            95: ("⛈️", "Thunderstorm"),
            96: ("⛈️", "Thunderstorm with slight hail"),
            99: ("⛈️", "Thunderstorm with heavy hail"),
        }
        return wmo_mapping.get(code, ("🌍", "Unknown Weather Pattern"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())