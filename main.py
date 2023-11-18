import streamlit as st

from streamlit_option_menu import option_menu
from widget.login import __login__
from menu.homepage import Homepage
from menu.database import Database

st.set_page_config(
    page_title='CJ OliveNetworks CloudWave', 
    page_icon="./images/cj-olivenetworks.png", 
    layout="wide", 
    initial_sidebar_state="expanded", 
    menu_items=None
)

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def side_bar():
    with st.sidebar.container():
        selected_page = option_menu(
            "Main Menu", ["Main_Home", "Database_Home"],
            icons=['bi bi-house', 'bi bi-database-check'],
            menu_icon="cast", 
            default_index=1,
            styles={
                "container": {"padding": "4!important", "background-color": "#fafafa"},
                "icon": {"color": "black", "font-size": "20px"},
                "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
                "nav-link-selected": {"background-color": "#08c7b4"}
            }
        )
        if st.button('Logout', use_container_width=True):
        # 로그인 상태를 False로 설정하고 리디렉션
            st.session_state['logged_in'] = False
            st.rerun()
    return selected_page

# def logged_out():
#     with st.sidebar.container():
#         if st.button('Logout', use_container_width=True):
#         # 로그인 상태를 False로 설정하고 리디렉션
#             st.session_state['logged_in'] = False
#             st.experimental_rerun()

def main():
    if st.session_state['logged_in'] == True:
        selected_page = side_bar()
        # logged_out()
        if selected_page == 'Main_Home':
            Homepage()
        elif selected_page == 'Database_Home':
            Database()
    else:
        __login__()
    
if __name__ == "__main__":
    main()