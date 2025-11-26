import requests
from typing import Tuple, Optional

class AirQualityAPI:
    """
    Professional wrapper for the OpenAQ API.
    Fetches real-time PM2.5 data and calculates health impact.
    """
    
    def __init__(self):
        self.base_url = "https://api.openaq.org/v2"
    
    def get_nearby_measurements(self, lat: float, lon: float, radius_km: int = 10) -> Optional[float]:
        """
        Fetches PM2.5 data.
        Returns: Average PM2.5 (float) or None if API fails.
        """
        try:
            url = f"{self.base_url}/measurements"
            params = {
                "coordinates": f"{lat},{lon}",
                "radius": radius_km * 1000,
                "parameter": "pm25",
                "limit": 5, 
                "order_by": "datetime",
                "sort": "desc"
            }
            
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                if results:
                    values = [r['value'] for r in results if r.get('value') is not None]
                    if values:
                        return round(sum(values) / len(values), 2)
            return None
            
        except Exception as e:
            print(f"⚠️ API Error: {e}")
            return None
    
    def get_health_impact(self, pm25_value: float) -> Tuple[str, str]:
        """Returns a tuple: (Category String, Color Code)"""
        if pm25_value is None: return "Unknown", "gray"
        if pm25_value <= 12: return "Good (Safe)", "green"
        if pm25_value <= 35: return "Moderate", "#FFC300" # Amber
        if pm25_value <= 55: return "Unhealthy for Sensitive", "orange"
        if pm25_value <= 150: return "Unhealthy", "red"
        return "Hazardous", "purple"

    def calculate_cigarettes(self, pm25_diff: float, duration_min: float) -> float:
        """
        Converts PM2.5 exposure to 'Cigarettes Smoked' equivalent.
        Scientific Rule of Thumb: ~22 ug/m3 for 24 hours ~= 1 cigarette.
        """
        if not pm25_diff: return 0.0
        
        # Calculate fraction of the day spent commuting
        day_fraction = duration_min / (24 * 60)
        
        # Calculate effective cigarettes
        # We take absolute value to show magnitude, direction handled in UI
        cigs = (abs(pm25_diff) / 22) * day_fraction
        return round(cigs, 4)