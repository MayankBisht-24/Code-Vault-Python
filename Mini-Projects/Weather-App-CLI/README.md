<div align="center">

<!-- Animated typing header -->
<a href="https://github.com/">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&pause=1000&color=00A8E8&center=true&vCenter=true&width=600&lines=Weather+App+(CLI);Live+Weather+Straight+From+Your+Terminal;Built+with+Python+%F0%9F%90%8D" alt="Typing SVG" />
</a>

<br/>

<!-- Badges -->
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-2.34-green?style=for-the-badge&logo=python&logoColor=white)
![OpenWeatherMap](https://img.shields.io/badge/API-OpenWeatherMap-orange?style=for-the-badge&logo=cloudflare&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

</div>

---

## 📖 About the Project

**Weather App (CLI)** is a lightweight command-line tool that fetches and displays **live weather data** for any city in the world using the OpenWeatherMap API.

Built as part of a hands-on Python learning journey, this project focuses on writing clean, modular code with proper error handling — the kind of practices used in real production-level applications.

No clutter, no unnecessary dependencies — just clean requests, clean output, and a clear structure.

---

## ✨ Features

- 🌍 Fetch real-time weather data for **any city** worldwide
- 🌡️ Displays temperature, feels-like, humidity, wind speed, and pressure
- 🌅 Shows accurate sunrise & sunset times (adjusted to the city's own timezone)
- 🔐 API key kept secure using environment variables (`.env`)
- ⚠️ Robust error handling for invalid cities, timeouts, and connection issues
- 🧩 Fully modular code — easy to read, extend, and maintain

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Requests](https://img.shields.io/badge/-Requests-000000?style=flat-square&logo=python&logoColor=white)
![dotenv](https://img.shields.io/badge/-python--dotenv-ECD53F?style=flat-square&logo=dotenv&logoColor=black)

| Tool | Purpose |
|------|---------|
| `requests` | Handling HTTP requests to the OpenWeatherMap API |
| `python-dotenv` | Securely loading the API key from a `.env` file |
| `OpenWeatherMap API` | Source of live weather data |

---

## 📂 Project Structure

```
Weather-App-CLI/
├── weather_app.py       # Main application logic
├── .env                 # Stores API key (not committed to Git)
├── .gitignore            # Files/folders excluded from version control
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/Weather-App-CLI.git
cd Weather-App-CLI
```

### 2. Create a virtual environment
```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows**
```bash
venv\Scripts\activate
```

**macOS / Linux**
```bash
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Set up your API key
Get a free API key from [OpenWeatherMap](https://openweathermap.org/api), then open the `.env` file and add:
```
OPENWEATHER_API_KEY=your_api_key_here
```

### 6. Run the application
```bash
python weather_app.py
```

---

## 🖥️ Usage

Once running, simply type the name of any city when prompted:

```
==============================
        Weather App
==============================

Enter City Name: Delhi

City          : Delhi
Country       : IN
Temperature   : 34°C
Feels Like    : 37°C
Condition     : Clouds
Description   : Broken Clouds
Humidity      : 62%
Wind Speed    : 4.8 m/s
Pressure      : 1008 hPa
Visibility    : 10 km
Sunrise       : 05:28 AM
Sunset        : 07:18 PM
```

---

## 🚨 Error Handling

This project gracefully handles the following scenarios:

| Scenario | Behavior |
|----------|----------|
| Empty city input | Prompts an error message and exits |
| Invalid city name | Returns a clear "city not found" message |
| No internet connection | Catches `ConnectionError` |
| API request timeout | Catches `Timeout` and notifies the user |
| Invalid or missing API key | Detects `401 Unauthorized` and gives guidance |

---

## 🚀 Future Improvements

- [ ] Add support for a 5-day weather forecast
- [ ] Add unit selection (Celsius / Fahrenheit toggle)
- [ ] Build a GUI version using Tkinter or a web version using Flask
- [ ] Cache recent searches for faster repeated lookups

---

## 👤 Author

**Mayank Bisht**
BCA Student — Data Science Specialization

<p align="left">
  <img src="https://img.shields.io/badge/Learning-Python-blue?style=flat-square" />
  <img src="https://img.shields.io/badge/Focused%20on-Data%20Science-purple?style=flat-square" />
</p>

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and build on it.

---

<div align="center">

⭐ If you found this project useful, consider giving it a star on GitHub!

</div>