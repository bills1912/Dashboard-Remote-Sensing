import streamlit as st
from multiapp import MultiApp
from apps import (
    gee,
    home
)

st.set_page_config(layout="wide")


apps = MultiApp()

# Add all your application here

apps.add_app("Home", home.app)
apps.add_app("Google Earth Engine (GEE)", gee.app)

# The main app
apps.run()
