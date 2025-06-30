import streamlit as st
from backend.model_predict import *


def main():
    '''# Execute your series of scripts
    Script_fetch_from_db.run()
    Parse.run()
    process.run()
    dataprocess.run()
    laggeddata.run()
    weatherunion_script.run()
    model_predict.run()
    '''
    regions = predicted_values
    cols = st.columns(len(regions))


    for i, (region, value) in enumerate(regions.items()):
        with cols[i]:
            st.button(str(value), key=f"btn_{region}")
            st.write(region) 





