# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 16:00:05 2023

@author: Thuy-trang
"""
#__import__('pysqlite3')
#import sys
#sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import streamlit as st
#import openai
import os
import requests
#from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
#from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.docstore.document import Document


os.environ["OPENAI_API_KEY"] = "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"
api_key = "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"


st.header("Support Client 💬 📚")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Bienvenue chez Bonjour Patrimoine"}
    ]
    
@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading information – hang tight! This should take 1-2 minutes."):
        loader = DirectoryLoader("SOURCE_DOCUMENTS/")
        index = VectorstoreIndexCreator().from_loaders([loader])
        return index
    
index = load_data()
if question := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": question})

for message in st.session_state.messages: 
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            prompt = f"User Query: {question}\n\nContext: Give long and more detailed answer "
            response = index.query(prompt, llm = ChatOpenAI(model="gpt-4-1106-preview"))
            engine_link = "https://api.openai.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {api_key}"}
            prompt = f"Please provide a friendly , commercial , detailed answer in French base on only the content of {response}. You are the assistant of company Bonjour Patrimoine,whose contact is 05 61 52 17 01 and website is https://gestiondepatrimoine.com/ , not give wrong information such as contact@gestiondepatrimoine.com , PYRENEES FINANCE CONSEIL et CGP ONE in the answer.  \n\nQuestion: {question}\nAnswer:"
            payload = {
                "messages": [
                    {"role": "system", "content": f"OpenAI/gpt-4-1106-preview"},
                    {"role": "user", "content": prompt}
            ],
                "model": "gpt-4-1106-preview",
            }
            response2 = requests.post(engine_link, headers=headers, json=payload)
            if response2.status_code == 200:
                response_data = response2.json()
                response = response_data["choices"][0]["message"]["content"]
                st.write(response)
                message = {"role": "assistant", "content": response}
            else:
                st.error(f"Error: {response.status_code} - {response.reason}")
                st.write(response)
                message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)
