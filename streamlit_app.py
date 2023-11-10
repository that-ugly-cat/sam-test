import openai
from openai import OpenAI
import streamlit as st
client = OpenAI()


# Set OpenAI API key from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]

with st.sidebar:
    st.write("Just an empty sidebar I might use later")

st.title("💬 Talk to Sam") 
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
    ##
    st.write(st.session_state["messages"])
    ##

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

#logic
if prompt := st.chat_input():
    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    
    msg_role = response.choices[0].message.role
    msg_content = response.choices[0].message.content

    msg = {'role' : msg_role, 'content' : msg_content}
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg_content)
