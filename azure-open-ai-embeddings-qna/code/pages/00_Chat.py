import streamlit as st
from streamlit_chat import message
from utilities.helper import LLMHelper

def format_source_url(url):
    return url.replace('/converted', '').replace('.txt', '')

def clear_text_input():
    st.session_state['question'] = st.session_state['input']
    st.session_state['input'] = ""

def clear_chat_data():
    st.session_state['input'] = ""
    st.session_state['chat_history'] = []
    st.session_state['source_documents'] = []
    st.experimental_rerun() #新增, 避免清除不完整

# Initialize chat history
if 'question' not in st.session_state:
    st.session_state['question'] = None
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'source_documents' not in st.session_state:
    st.session_state['source_documents'] = []

llm_helper = LLMHelper()

# Chat 
st.text_input("You: ", placeholder="type your question", key="input", on_change=clear_text_input)
clear_chat = st.button("Clear chat", key="clear_chat", on_click=clear_chat_data)

if st.session_state['question']:
    question, result, _, sources = llm_helper.get_semantic_answer_lang_chain(st.session_state['question'], st.session_state['chat_history'])
    st.session_state['chat_history'].append((question, result))
    st.session_state['source_documents'].append(list(map(format_source_url, sources)))

if st.session_state['chat_history']:
    for i in range(len(st.session_state['chat_history'])):
        message(st.session_state['chat_history'][i][0], is_user=True, key=str(i) + '_user')
        message(st.session_state['chat_history'][i][1], key=str(i))
        st.markdown(f'\n\nSources: {st.session_state["source_documents"][i]}')

# if st.session_state['chat_history']:
#     for i in range(len(st.session_state['chat_history'])-1, -1, -1):
#         message(st.session_state['chat_history'][i][1], key=str(i))
#         st.markdown(f'\n\nSources: {st.session_state["source_documents"][i]}')
#         message(st.session_state['chat_history'][i][0], is_user=True, key=str(i) + '_user')
