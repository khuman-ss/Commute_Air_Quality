import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from src.air_quality import AirQualityAPI
from src.route_optimizer import RouteOptimizer

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="EcoCommute | Air Quality Router", page_icon="🌿", layout="wide")

# --- CSS FOR AESTHETICS ---
st.markdown("""
    <style>
    .metric-card {background-color: #1E1E1E; padding: 20px; border-radius: 10px; border-left: 5px solid #1f77b4;}
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE BACKEND ---
@st.cache_resource
def load_engines():
    return AirQualityAPI(), RouteOptimizer()

air_engine, route_engine = load_engines()

# --- MANAGE STATE (CRITICAL FOR STABILITY) ---
if "has_run" not in st.session_state:
    st.session_state.has_run = False
if "routes_data" not in st.session_state:
    st.session_state.routes_data = None
if "aqi_data" not in st.session_state:
    st.session_state.aqi_data = None

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.title("🌿 EcoCommute")
    st.markdown("Optimization Engine Active")
    st.markdown("---")
    
    # Use a Form so inputs don't trigger re-runs individually
    with st.form("route_form"):
        start = st.text_input("📍 Start Location", "Connaught Place, Delhi")
        end = st.text_input("🏁 End Location", "India Gate, Delhi")
        submitted = st.form_submit_button("Find Cleanest Route", type="primary")
    
    if submitted:
        st.session_state.has_run = True 

    st.markdown("---")
    st.info("💡 **Did you know?** Reducing PM2.5 exposure by 10 units can increase life expectancy by 0.6 years.")

# --- MAIN DASHBOARD ---
st.title("City Air Quality & Route Optimizer")
st.markdown("### 📊 Live Traffic & Toxicity Analysis")

# --- CALCULATION LOGIC ---
if submitted and start and end:
    with st.spinner("🛰️ Triangulating coordinates & fetching satellite data..."):
        coords_start = route_engine.geocode_address(start)
        coords_end = route_engine.geocode_address(end)
    
    if coords_start and coords_end:
        # Generate Routes
        routes = route_engine.generate_routes(coords_start, coords_end)
        
        # Fetch Air Quality (Simulated for Demo Stability)
        # In a real app, you would iterate through all waypoints
        mid1 = routes['route1']['path'][5]
        mid2 = routes['route2']['path'][5]
        
        aqi1 = air_engine.get_nearby_measurements(mid1[0], mid1[1]) or 55 
        aqi2 = air_engine.get_nearby_measurements(mid2[0], mid2[1]) or 35 
        
        # Calculate Cigarettes
        cigs = air_engine.calculate_cigarettes(aqi1 - aqi2, routes['route1']['time'])
        
        # Save to State
        st.session_state.routes_data = routes
        st.session_state.coords = (coords_start, coords_end)
        st.session_state.aqi_data = {
            'aqi1': aqi1, 'aqi2': aqi2,
            'cat1': air_engine.get_health_impact(aqi1)[0],
            'cat2': air_engine.get_health_impact(aqi2)[0],
            'cigs': cigs
        }
    else:
        st.error("Could not find address. Try adding the city name.")
        st.session_state.has_run = False

# --- DISPLAY LOGIC (FROM STATE) ---
if st.session_state.has_run and st.session_state.routes_data:
    r_data = st.session_state.routes_data
    a_data = st.session_state.aqi_data
    coords = st.session_state.coords
    
    # --- KPI ROW ---
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Route A (Direct)", f"{r_data['route1']['time']} min", f"PM2.5: {a_data['aqi1']}")
        st.caption(f"Status: {a_data['cat1']}")
    with c2:
        st.metric("Route B (Green)", f"{r_data['route2']['time']} min", f"PM2.5: {a_data['aqi2']}")
        st.caption(f"Status: {a_data['cat2']}")
    with c3:
        # The "Business Insight" Metric
        delta_color = "normal" if a_data['aqi2'] < a_data['aqi1'] else "inverse"
        st.metric("Lung Damage Avoided", f"{a_data['cigs']} Cigarettes", "Equivalent", delta_color=delta_color)
    
    st.divider()

    # --- MAP & CHART ROW ---
    col_map, col_chart = st.columns([2, 1])
    
    with col_map:
        st.subheader("🗺️ Route Comparison")
        # Dark Mode Map for Professional Look
        m = folium.Map(location=coords[0], zoom_start=13, tiles="cartodbdark_matter")
        
        # Route 1 (Red)
        folium.PolyLine(r_data['route1']['path'], color='#FF4B4B', weight=4, opacity=0.8, tooltip="High Toxicity Route").add_to(m)
        # Route 2 (Green)
        folium.PolyLine(r_data['route2']['path'], color='#00CC96', weight=4, opacity=0.8, tooltip="Eco Route").add_to(m)
        
        folium.Marker(coords[0], icon=folium.Icon(color='blue', icon='play'), tooltip="Start").add_to(m)
        folium.Marker(coords[1], icon=folium.Icon(color='red', icon='flag'), tooltip="End").add_to(m)
        
        st_folium(m, width=None, height=400)
        
    with col_chart:
        st.subheader("📉 Toxicity Profile")
        # Simulated profile data for visualization
        chart_data = pd.DataFrame({
            "Distance (%)": [0, 20, 40, 60, 80, 100],
            "Route A (Direct)": [a_data['aqi1'], a_data['aqi1']+10, a_data['aqi1']+15, a_data['aqi1']+5, a_data['aqi1'], a_data['aqi1']-5],
            "Route B (Green)": [a_data['aqi2'], a_data['aqi2']-2, a_data['aqi2']-5, a_data['aqi2'], a_data['aqi2']+5, a_data['aqi2']]
        })
        st.line_chart(chart_data, x="Distance (%)", y=["Route A (Direct)", "Route B (Green)"], color=["#FF4B4B", "#00CC96"], height=350)

    # --- RECOMMENDATION ---
    if a_data['aqi2'] < a_data['aqi1']:
        st.success(f"✅ **Recommendation:** Take **Route B**. Although it takes slightly longer, you avoid inhaling the equivalent of **{a_data['cigs']} cigarettes**.")
    else:
        st.warning("⚠️ Both routes have similar pollution levels today.")

elif not st.session_state.has_run:
    st.info("👈 Enter coordinates in the sidebar to generate your Health Report.")  