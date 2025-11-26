from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from typing import Tuple, Dict, Any, List, Optional

class RouteOptimizer:
    """
    Handles Geocoding and Route Simulation logic.
    """
    
    def __init__(self):
        # User-agent is required by Nominatim policy
        self.geolocator = Nominatim(user_agent="eco_commute_portfolio_v1")
    
    def geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """Converts text address to (lat, lon)"""
        try:
            location = self.geolocator.geocode(address, timeout=10)
            return (location.latitude, location.longitude) if location else None
        except:
            return None
    
    def generate_routes(self, start: Tuple[float, float], end: Tuple[float, float]) -> Dict[str, Any]:
        """
        Simulates two routes: 
        1. Direct (Faster, usually busier/polluted)
        2. Alternate (Slightly longer, potentially cleaner)
        """
        dist_km = geodesic(start, end).kilometers
        
        # Route 1: Direct Line Simulation
        route1_waypoints = self._create_waypoints(start, end, offset=0)
        
        # Route 2: Curved Path (Simulating a detour)
        route2_waypoints = self._create_waypoints(start, end, offset=0.03) # 0.03 deg offset
        
        return {
            'route1': {
                'path': route1_waypoints,
                'dist': round(dist_km, 2),
                'time': round((dist_km/30)*60, 0) # Avg 30km/h city speed
            },
            'route2': {
                'path': route2_waypoints,
                'dist': round(dist_km * 1.2, 2), # 20% longer
                'time': round(((dist_km * 1.2)/35)*60, 0) # Faster speed on detour
            }
        }

    def _create_waypoints(self, start: Tuple[float, float], end: Tuple[float, float], offset: float) -> List[Tuple[float, float]]:
        """Helper to generate map coordinates"""
        path = []
        for i in range(11): # Increased points for smoother lines
            frac = i / 10
            lat = start[0] + (end[0] - start[0]) * frac
            lon = start[1] + (end[1] - start[1]) * frac
            
            # Add curve for Route 2 logic
            if offset > 0:
                # Simple sine-wave like curve logic using parabola
                curve = (1 - (2 * frac - 1)**2) * offset
                lat += curve
                
            path.append((lat, lon))
        return path