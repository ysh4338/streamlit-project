import streamlit as st
import bedrock

#Home Page Information
st.set_page_config(
    page_title="CJ OliveNetworks",
    page_icon="./images/cj-olivenetworks.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get help': 'https://python.langchain.com/docs/use_cases/summarization',
        'Report a bug': "https://github.com/langchain-ai",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)
st.title('CJ CloudWave')
st.header('Generative AI System')

#Home Page Side-Bar Information Section 
st.sidebar.title("LLM Settings")

placeholder = st.empty()

if 'conversation_model' not in st.session_state:
    # st.session_state['conversation_model'] = bedrock.get_bedrock_agent()
    # st.session_state['conversation_model'] = bedrock.get_bedrock_basic()
    st.session_state['conversation_model'] = bedrock.get_bedrock_history()

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요. CJ OliveNetworks 입니다. 무엇을 도와드릴까요?"}]

conversation = st.session_state['conversation_model']

with placeholder.container():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
             st.write(message["content"])

    if prompt := st.chat_input('Enter Your Prompt'):
        chat_history = st.session_state.messages[-10:]
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = conversation.run(input=prompt, history=chat_history)
        st.chat_message("assistant").write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})