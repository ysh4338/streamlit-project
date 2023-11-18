import streamlit as st

class AboutPage:
    def __init__(self):
        self.about_page()

    def about_page(self):
        st.title("About")
        st.header('Generative AI System')
        st.write("This is the about page.")