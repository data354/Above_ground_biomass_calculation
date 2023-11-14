#import gradio as gr
import streamlit as st
import pandas as pd
import numpy as np
from above_ground import *



#title = "🌴 ABOVE GROUND BIOMASS CALCULATION WITH FIELD DATA 🌴"
#description = "."
# 🌷🌸🌹🌺🌻🌼
#article = "Created by data354.

st.title("🌴 AGBD CALCULATION 🌴")
st.markdown("In this application we use field measurement to calculate aboveground biomass density (AGBD) using allometric equations.")
uploaded_file = st.file_uploader("Upload your file here...", type=['csv','xlsx'])

if uploaded_file is not None:
  #pd.read_excel(uploaded_file,sheet_name="GIZ FR Biomass plots_ Carbon...")
    shade_trees_biomass = shade_tree_biomass(uploaded_file)
    cocoa_trees_biomass = cocoa_tree_biomass(uploaded_file)
    biomass_total = biomass_finale(shade_trees_biomass,cocoa_trees_biomass,"version_test")

    st.write(biomass_total)
  


