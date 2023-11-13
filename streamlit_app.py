import openai
from openai import OpenAI
import streamlit as st
client = OpenAI()


# Set OpenAI API key from Streamlit secrets
openai_api_key = st.secrets["OPENAI_API_KEY"]


st.title("💬 Talk to Sam") 
if "messages" not in st.session_state:
    with open('persona.txt') as f:
        persona = f.read()
    st.session_state["messages"] = [{"role": "system", "content": persona}, {"role": "assistant", "content": "Hi, I am Sam. I am a synthetic patient, based on the work of Giovanni Spitale, Gerold Schneider, Federico Germani, and Nikola Biller Andorno. Feel free to ask me about my experiece as a patient. Also, I speak English, Italian, German, and French."}]


for msg in st.session_state.messages:
    if msg['role'] != 'system':
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
