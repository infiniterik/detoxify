import streamlit as st

import requests
import json

if "model" not in st.session_state:
    st.session_state.model = "chatgpt"
 
 
headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": "Bearer my-secret"
}

st.title("D-ESC Detoxifier")

col1, col2 = st.columns(2)

with col2:
    st.radio("Select Model 👇", ["chatgpt", "pcts"], key="model")

with col1:
    st.header(st.session_state.model)
    if st.session_state.model == "pcts":
        parent = st.text_area('Parent', '''Enter parent post here''')
        st.radio("Parent post toxicity ☣️", ["toxic", "non-toxic"], key="parent_toxicity")
    post = st.text_area('Post', '''Enter post here''')
    if st.button('Detoxify!'):
        with st.spinner("Detoxifying..."):
            if st.session_state.model == "pcts":
                url = f"http://localhost:8000/t5"
                response = requests.post(url, headers=headers, json={
                    "model": st.session_state.model,
                    "parent": parent,
                    "parent_toxicity": st.session_state.parent_toxicity,
                    "post": post
                })
            else:
                url = f"http://localhost:8000/{st.session_state.model}"
                response = requests.post(url, headers=headers, json={
                    "post": post
                })
        st.json(response.text)

        