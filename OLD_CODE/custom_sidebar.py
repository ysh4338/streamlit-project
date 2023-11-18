import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title='CJ OliveNetworks - CloudWave', 
    page_icon="./images/cj-olivenetworks.png", 
    layout="wide", 
    initial_sidebar_state="expanded", 
    menu_items=None
)

with st.sidebar:
    st.sidebar.title('Public Cloud Class')
    choice = option_menu("Menu", ["Route53", "RDS_MYSQL", "Auto Scaling"],
                         icons=['bi bi-1-circle', 'kanban', 'bi bi-robot'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "4!important", "background-color": "#fafafa"},
        "icon": {"color": "black", "font-size": "20px"},
        "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#08c7b4"},
    }
    )