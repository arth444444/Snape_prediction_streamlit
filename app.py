import streamlit as st
from model_predict import *
import sys
import traceback
from datetime import datetime, timedelta
import pytz

st.set_page_config(page_title="Demand Prediction", layout="wide")

def get_prediction_time():
    """Calculate the prediction time (current time + 1 hour) in IST"""
    # Get current time in IST (Indian Standard Time)
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist)
    prediction_time = current_time + timedelta(hours=1)
    
    return current_time, prediction_time

def main():
    st.title("🚖 Kolkata Taxi Demand Prediction Dashboard")
    
    # Get time information
    current_time, prediction_time = get_prediction_time()
    
    # Display time information in a prominent way
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(
            f"""
            <div style="text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px; margin: 20px 0;">
                <h3 style="color: #1f77b4; margin-bottom: 10px;">⏰ Prediction Timeline</h3>
                <p style="font-size: 18px; margin: 5px 0;"><strong>Current Time:</strong> {current_time.strftime('%I:%M %p, %B %d, %Y')}</p>
                <p style="font-size: 20px; color: #e74c3c; margin: 5px 0;"><strong>Demand Predicted for:</strong> {prediction_time.strftime('%I:%M %p, %B %d, %Y')}</p>
                <small style="color: #7f8c8d;">Predictions are made 1 hour in advance</small>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    try:
        with st.spinner("🔄 Loading data and running predictions..."):
            # Import after Streamlit setup to ensure proper initialization
            from model_predict import predicted_values
            
        st.success("✅ Predictions completed successfully!")
        
        # Separate the 5 zones from total city demand
        zone_predictions = {k: v for k, v in predicted_values.items() if k != 'kolkata_city'}
        total_city_demand = predicted_values.get('kolkata_city', 0)
        
        # Display total city demand prominently
        st.markdown("### 🏙️ Total Kolkata City Demand")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                f"""
                <div style="text-align: center; padding: 25px; background-color: #e8f4fd; border-radius: 15px; border: 2px solid #1f77b4;">
                    <h2 style="color: #1f77b4; margin: 0;">{int(max(0, total_city_demand))} Rides</h2>
                    <p style="font-size: 18px; color: #2c3e50; margin: 10px 0;">Expected in next hour across all Kolkata</p>
                    <small style="color: #7f8c8d;">This includes all 5 zones + other areas</small>
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        st.markdown("---")
        
        # Display zone-wise predictions
        st.markdown("### 📊 Zone-wise Demand Breakdown")
        st.markdown(f"*Demand forecast for {prediction_time.strftime('%I:%M %p')} across 5 key zones*")
        
        # Create responsive columns for the 5 zones
        cols = st.columns(3)  # 3 columns for better layout
        
        # Zone name mapping for better display
        zone_display_names = {
            'airport': '🛫 Airport Area',
            'laketown': '🏘️ Lake Town',
            'sectorV': '🏢 Sector V',
            'victoria': '🏛️ Victoria Memorial',
            'howrah': '🚂 Howrah Station'
        }
        
        for i, (region, value) in enumerate(zone_predictions.items()):
            col_index = i % len(cols)
            with cols[col_index]:
                # Get display name or use original if not in mapping
                display_name = zone_display_names.get(region, region.replace('_', ' ').title())
                
                # Create a metric card with color coding based on demand level
                demand_value = int(value) if value > 0 else 0
                
                # Color coding based on demand level for zones
                if demand_value >= 30:
                    delta_color = "normal"  # Green
                    status = "🔥 High"
                elif demand_value >= 15:
                    delta_color = "off"     # Gray
                    status = "📈 Medium"
                else:
                    delta_color = "inverse" # Red
                    status = "📉 Low"
                
                st.metric(
                    label=display_name,
                    value=f"{demand_value}",
                    delta=status,
                    delta_color=delta_color
                )
        
        # Zone-based insights and recommendations
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Zone Analysis")
            zone_demands = [(zone, max(0, int(demand))) for zone, demand in zone_predictions.items()]
            zone_demands.sort(key=lambda x: x[1], reverse=True)
            
            st.write(f"**Total Zone Demand:** {sum(d[1] for d in zone_demands)} rides")
            
            if zone_demands:
                highest_zone = zone_demands[0]
                lowest_zone = zone_demands[-1]
                
                st.write(f"**Highest Demand Zone:** {zone_display_names.get(highest_zone[0], highest_zone[0])} ({highest_zone[1]} rides)")
                st.write(f"**Lowest Demand Zone:** {zone_display_names.get(lowest_zone[0], lowest_zone[0])} ({lowest_zone[1]} rides)")
                
                # Calculate percentage distribution
                total_zone_demand = sum(d[1] for d in zone_demands)
                if total_zone_demand > 0:
                    highest_percentage = (highest_zone[1] / total_zone_demand) * 100
                    st.write(f"**Top Zone Share:** {highest_percentage:.1f}% of zone demand")
        
        with col2:
            st.markdown("### 🎯 Driver Deployment Recommendations")
            
            # Find high and low demand zones among the 5 zones only
            high_demand_zones = [zone for zone, demand in zone_predictions.items() if demand >= 20]
            medium_demand_zones = [zone for zone, demand in zone_predictions.items() if 10 <= demand < 20]
            low_demand_zones = [zone for zone, demand in zone_predictions.items() if demand < 10]
            
            if high_demand_zones:
                zone_names = [zone_display_names.get(z, z) for z in high_demand_zones]
                st.success(f"**🚀 Priority Deployment:** {', '.join(zone_names)}")
                st.info("💡 **Action:** Deploy maximum drivers to these zones")
            
            if medium_demand_zones:
                zone_names = [zone_display_names.get(z, z) for z in medium_demand_zones]
                st.warning(f"**📈 Standard Deployment:** {', '.join(zone_names)}")
            
            if low_demand_zones:
                zone_names = [zone_display_names.get(z, z) for z in low_demand_zones]
                st.info(f"**📉 Minimal Deployment:** {', '.join(zone_names)}")
        
        # Additional city-wide insights
        st.markdown("---")
        st.markdown("### 🌆 City-wide Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Calculate zone coverage percentage
            total_zone_demand = sum(max(0, int(v)) for v in zone_predictions.values())
            zone_coverage = (total_zone_demand / max(1, total_city_demand)) * 100 if total_city_demand > 0 else 0
            
            st.metric(
                label="🎯 Zone Coverage",
                value=f"{zone_coverage:.1f}%",
                delta="of total city demand"
            )
        
        with col2:
            # Average demand per zone
            avg_zone_demand = total_zone_demand / len(zone_predictions) if zone_predictions else 0
            
            st.metric(
                label="📊 Avg Zone Demand",
                value=f"{avg_zone_demand:.1f}",
                delta="rides per zone"
            )
        
        with col3:
            # Peak zone indicator
            if zone_predictions:
                peak_zone = max(zone_predictions.items(), key=lambda x: x[1])
                peak_zone_name = zone_display_names.get(peak_zone[0], peak_zone[0])
                
                st.metric(
                    label="🏆 Peak Zone",
                    value=peak_zone_name.split(' ')[-1],  # Get last word for brevity
                    delta=f"{int(peak_zone[1])} rides"
                )
        
        # Show last updated time
        st.markdown("---")
        st.caption(f"🕒 Last updated: {current_time.strftime('%I:%M:%S %p IST')} | Next update in: {60 - current_time.minute} minutes")
        st.caption("📍 **Note:** Total city demand includes the 5 tracked zones plus other areas across Kolkata")
        
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        with st.expander("🔍 See error details"):
            st.code(traceback.format_exc())
        
        # Provide debugging information
        st.markdown("### 🛠️ Troubleshooting Guide")
        st.info("""
        **Common Issues & Solutions:**
        1. **Model Loading Error:** Ensure all `.h5` model files are in the `models/` directory
        2. **Data Connection Error:** Check internet connectivity for weather API calls
        3. **Prediction Error:** Verify that input data format matches training data
        4. **Time Zone Error:** Ensure `pytz` is installed (`pip install pytz`)
        
        **File Structure:**
        ```
        your_project/
        ├── app.py
        ├── model_predict.py
        ├── weatherunion_script.py
        ├── models/
        │   ├── lstm_airport.h5
        │   ├── scaler_x_airport.pkl
        │   └── ... (other model files)
        └── requirements.txt
        ```
        """)

if __name__ == "__main__":
    main()