import streamlit as st
import subprocess
from pathlib import Path
import sys

build_dir = Path('build')
llama_cli = build_dir / 'bin' / 'llama-cli'

if 'llm' not in st.session_state:
    st.session_state.llm = subprocess.Popen(
        args=[str(llama_cli)] + sys.argv[1:],
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    next_token = st.session_state.llm.stdout.read(1)
    while next_token != '>':
        next_token = st.session_state.llm.stdout.read(1)
    print("LLM is Ready")


def llm_response():
    next_token = st.session_state.llm.stdout.read(1)
    while next_token != '>':
        next_token = st.session_state.llm.stdout.read(1)
        yield next_token


st.title("BitNet on Graviton")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Pass to llamaci
    st.session_state.llm.stdin.write(prompt + '\n')
    st.session_state.llm.stdin.flush()
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(llm_response())
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
