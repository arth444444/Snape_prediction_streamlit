import streamlit as st
from model_predict import *
import sys
import traceback

st.set_page_config(page_title="Demand Prediction", layout="wide")

def main():
    st.title("🚖 Demand Prediction Dashboard")
    
    try:
        with st.spinner("Loading data and running predictions..."):
            # Import after Streamlit setup to ensure proper initialization
            from model_predict import predicted_values
            
        st.success("✅ Predictions completed successfully!")
        
        # Display predictions in a nice grid
        st.markdown("### 📊 Predicted Demand by Zone")
        
        regions = predicted_values
        cols = st.columns(len(regions))
        
        for i, (region, value) in enumerate(regions.items()):
            with cols[i]:
                # Create a metric card
                st.metric(
                    label=region.replace('_', ' ').title(),
                    value=f"{int(value)}",
                    delta=None
                )
                
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        with st.expander("See error details"):
            st.code(traceback.format_exc())
        
        # Provide debugging information
        st.info("""
        **Troubleshooting tips:**
        1. Make sure your BigQuery credentials are properly set in `.streamlit/secrets.toml`
        2. Ensure all model files are in the `models/` directory
        3. Check that you have internet connectivity for API calls
        4. Verify that the BigQuery dataset has data for the last 25 hours
        """)

if __name__ == "__main__":
    main()




