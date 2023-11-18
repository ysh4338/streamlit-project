import streamlit as st
from login.widgets import __login__

from menu.chatbot import Chatbot
from menu.chatbotRouter import ChatbotRouter
from menu.chatbotqa import ChatbotQA
from menu.chatbotagent import ChatbotAgent
from menu.chatbotPrompt import ChatbotPrompt
from menu.openSearch import OpenSearch
from streamlit_option_menu import option_menu

import langchain

langchain.debug = True

import sys
import os
#os.environ["OPENAI_API_KEY"] = "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"
os.environ["OPENAI_API_KEY"] = "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"
os.environ["HTTP_PROXY"] = "http://70.10.15.10:8080"
os.environ["HTTPS_PROXY"] = "http://70.10.15.10:8080"
#os.environ["REQUESTS_CA_BUNDLE"] = "C:/Users/SDS/MWG_Certification.crt"

module_path = ".."
sys.path.append(os.path.abspath(module_path))

st.set_page_config(page_title='bedrock poc', page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)

__login__obj = __login__(auth_token = "Temp",
                    company_name = "SamsungSDS",
                    width = 200, height = 250,
                    logout_button_name = 'Logout', hide_menu_bool = False,
                    hide_footer_bool = True,
                    #lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json'
                    lottie_url = ""
                    )

LOGGED_IN = __login__obj.build_login_ui()

def menuSidebar():
        """
        Creates the side navigaton bar
        """
        main_page_sidebar = st.sidebar.empty()
        with main_page_sidebar:
            selected_option = option_menu(
                menu_title = None,
                menu_icon = 'list-columns-reverse',
                #icons = ['box-arrow-in-right', 'person-plus', 'x-circle','arrow-counterclockwise'],
                options = ['Chatbot', 'Router', 'OpenSearch', 'QA', 'Agent', 'Pure-Prompt', 'PoC Flight'],
                styles = {
                    "container": {"padding": "5px"},
                    "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px"}} )
        return selected_option

if LOGGED_IN == True:      
    st.sidebar.title('Bedrock')
    
    selected_option = menuSidebar()

    if selected_option == 'Chatbot':
        Chatbot(__login__obj)
    # elif selected_option == 'PoC Flight':
    #     ChatbotFlight(__login__obj)
    elif selected_option == 'Router':
        ChatbotRouter(__login__obj)
    elif selected_option == 'OpenSearch':
        OpenSearch(__login__obj)
    elif selected_option == 'QA':
        ChatbotQA(__login__obj)
    elif selected_option == 'Agent':
        ChatbotAgent(__login__obj)
    elif selected_option == 'Pure-Prompt':
        ChatbotPrompt(__login__obj)
   






    


    
      