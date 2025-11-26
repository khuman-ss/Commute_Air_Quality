# 🌿 EcoCommute | Air Quality Route Optimizer

### 🏥 A "Google Maps for Health"
**EcoCommute** is a geospatial intelligence tool that helps urban commuters minimize toxic air exposure. Unlike standard navigation apps that optimize only for time, this engine calculates the "Health Cost" of a route by integrating real-time PM2.5 data from the **OpenAQ API**.

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![API](https://img.shields.io/badge/API-OpenAQ-green)

---

## 📊 Key Features
- **📉 Toxic Load Analysis:** Compares "Direct" vs. "Eco" routes to find the lowest pollution path.
- **🚬 Cigarette Equivalence Metric:** Translates abstract PM2.5 density ($\mu g/m^3$) into "Cigarettes Smoked" for immediate user impact.
- **🌑 Dark Mode Geospatial Viz:** Interactive **Folium** maps with dark-matter tiles for high-contrast data visualization.
- **⚡ Session State Management:** Optimized Streamlit backend to prevent reload loops during user interaction.

## 🛠️ Tech Stack
- **Frontend:** Streamlit, Streamlit-Folium
- **Geospatial:** Geopy, Folium
- **Data Pipeline:** Requests (OpenAQ API), Pandas
- **Architecture:** Modular Python (Separation of `src` logic and `app` UI)

## 🚀 How to Run Locally
1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/EcoCommute.git](https://github.com/YOUR_USERNAME/EcoCommute.git)