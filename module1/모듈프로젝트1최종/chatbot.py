from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import streamlit as st 
from dotenv import load_dotenv 
import os
import openai
from openai import OpenAI
key = ''


def app():

    st.title("🌱💬  SESAC BOT")

    # Initialize the chat messages history
    client = OpenAI(api_key=key)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Prompt for user input and save
    if prompt := st.chat_input("하고 싶은 말 입력"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            # for delta in openai.ChatCompletion.create(
            for delta in client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += delta.choices[0].delta.content if delta.choices[0].delta.content else ""

                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
