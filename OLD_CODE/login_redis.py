import requests
import streamlit as st

class __login__:
    def __init__(self):
        self.main()

    def check_login_status(self):
        # Flask 앱으로 현재 사용자의 세션 상태 확인 요청
        response = requests.get("http://localhost:5000/login")
        if response.ok and response.json().get('logged_in'):
            st.session_state['logged_in'] = True
        else:
            st.session_state['logged_in'] = False
        
    def login_form(self):
        with st.form("login_form"):
            username = st.text_input("Username",placeholder="Enter Username", label_visibility="collapsed")
            password = st.text_input("Password",placeholder="Password", type="password", label_visibility="collapsed")
            submitted = st.form_submit_button("Login In", use_container_width=True)

            if submitted:
                # Flask 앱으로 로그인 요청 보내기
                response = requests.post("http://localhost:5000/login", data={"username": username, "password": password})

                if response.ok and response.json().get('success'):
                    st.session_state['logged_in'] = True
                    st.success("Logged in successfully!")
                    st.rerun() 
                else:
                    st.error("Login failed. Please check your credentials.")
    
    def main(self):
        if 'logged_in' not in st.session_state:
            st.session_state['logged_in'] = self.check_login_status()

        st.markdown("<h1 style='text-align: center; color: #6495ED;'>Welcome</h1>", unsafe_allow_html=True)
        # self.nav_sidebar()

        col1, col2, col3 = st.columns([3.75, 2.5, 3.75])
        with col1:
            st.empty()

        with col2:
            st.markdown("<h4 style='text-align: center; color: black;'>Login Your Account</h4>", unsafe_allow_html=True)
            co1, co2, co3 = st.columns([4,1,5])
            with co1: st.empty()
            with co2: st.empty()
            with co3: st.empty()

            self.login_form()

        with col3:
            st.empty()
