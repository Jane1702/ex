import streamlit as st
#import openai
import os
#from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
#from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
os.environ["OPENAI_API_KEY"] = "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"


st.header("Trang's chatbot 💬 📚")

if "messages" not in st.session_state.keys(): # Initialize the chat message history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question"}
    ]
    
@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading information – hang tight! This should take 1-2 minutes."):
        loader = DirectoryLoader("SOURCE_DOCUMENTS/")
        index = VectorstoreIndexCreator().from_loaders([loader])
        return index
    
index = load_data()
if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = index.query(prompt, llm = ChatOpenAI(model="gpt-4-1106-preview"))
            st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)
