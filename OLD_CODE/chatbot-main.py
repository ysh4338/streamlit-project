import streamlit as st
import router

#Home Page Information
st.set_page_config(
    page_title="SAMSUNG AIRLINES",
    page_icon="./images/Anthropic-AI.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get help': 'https://python.langchain.com/docs/use_cases/summarization',
        'Report a bug': "https://github.com/langchain-ai",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
st.title('SAMSUNG AIRLINES')
st.header('Generative AI System')
print()

#Create new chat message history container
#If there ar existing messages in the session_state, does not create a new history container to avoid deleting history
placeholder = st.empty()

if 'conversation_router' not in st.session_state:
    st.session_state['conversation_router'] = router.get_router_chain()

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요. SAMSUNG AIRLINES 입니다. 무엇을 도와드릴까요?"}]

conversation = st.session_state['conversation_router']

with placeholder.container():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Enter your prompt"):
        chat_history = st.session_state.messages[-10:]
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
          
        response = conversation.run(prompt)
        st.chat_message("assistant").markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})