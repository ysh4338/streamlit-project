import streamlit as st
from login.widgets import __login__

from services import bedrock_service

from chains.router_chain_2_layer import getTestRounter2LayerChain

class ChatbotRouter:
   def __init__(self, __login__obj):
      self.setMainPage(__login__obj)

   def getBedrockConversation(self):
      st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you? this chatbot is for routing your question test"}]

      model = 'Anthropic Claude v2' if 'selectedBedrockModel' not in st.session_state else st.session_state['selectedBedrockModel']

      modelInfo = bedrock_service.get_bedrock_models_Information(model)
      claude_model_kwargs = {
                  "max_tokens_to_sample":1024,
                  "stop_sequences":['<< INPUT >>', '<< FORMATTING >>'],
                  "temperature":0,
                  "top_k":250,
                  "top_p":0
               }

      rllm = bedrock_service.get_bedrock_model(modelInfo[0], claude_model_kwargs)
      gllm = bedrock_service.get_bedrock_model(modelInfo[0], modelInfo[1])

      conversation = getTestRounter2LayerChain(rllm, gllm)

      print('\n Current Set LLM Info below : \n' + str(conversation))

      return conversation

   def changeModel(self):
      model = st.session_state['selectedBedrockModel']
      st.session_state['selectedBedrockModelIndex'] = list(bedrock_service.get_bedrock_models_Information().keys()).index(model)
      st.session_state['conversation'] = self.getBedrockConversation()

   def changeModelParam(self):
      model = st.session_state['selectedBedrockModel']
      conversation = st.session_state['conversation']
      modelParams = bedrock_service.get_bedrock_models_Information(model, 
                                                                   st.session_state['selectedTemperature'], 
                                                                   st.session_state['selectedTopP'],
                                                                   st.session_state['selectedMaxTokenSize']
                                                                   )[1]
      conversation.llm.model_kwargs = modelParams

      print('\n Current Set LLM Info below : \n' + str(conversation))

   def setSidebarPage(self, __login__obj):
      with st.sidebar:
         bedrockModels = bedrock_service.get_bedrock_models_Information()
         if 'selectedBedrockModelIndex' not in st.session_state:
            st.session_state['selectedBedrockModelIndex'] = 5
         
         st.selectbox('Model', bedrockModels.keys(), on_change=self.changeModel, index=st.session_state['selectedBedrockModelIndex'], key='selectedBedrockModel')
         st.slider('Temperature', 0.0, 1.0, 0.0, 0.1, key='selectedTemperature', on_change=self.changeModelParam)
         st.slider('TopP', 0.0, 1.0, 0.9, 0.1, key='selectedTopP', on_change=self.changeModelParam)
         st.slider('Maximum Response length', 0, 2048, 1024, key='selectedMaxTokenSize', on_change=self.changeModelParam)

      __login__.logout_widget(__login__obj)

   def setMainPage(self, __login__obj):
      placeholder = st.empty()

      if 'conversation_router' not in st.session_state:
         st.session_state['conversation_router'] = self.getBedrockConversation()

      if 'messages' not in st.session_state:
         st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you? this chatbot is for routing your question test"}]

      conversation = st.session_state['conversation_router']

      with placeholder.container():
         self.setSidebarPage(__login__obj)
         for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
         # for msg in conversation.memory.chat_memory.messages:
         #    type = "assistant" if msg.type=='ai' else "user"
         #    st.chat_message(type).write(msg.content)
         
         if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            response = conversation.run(input=prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.chat_message("assistant").write(response)
