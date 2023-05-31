import streamlit as st

import requests
import json

st.set_page_config(page_title="D-ESC Detoxifier", page_icon="☣️", layout="wide")
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)

if "model" not in st.session_state:
    st.session_state.model = "ChatGPT"
 
 
headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": "Bearer my-secret"
}

example_posts = {
    'None': ("Enter parent post here", "toxic", "Enter post here"),
    'Toxic Example 1': ("Abortion is murder. You should be ashamed of yourself!", "toxic", "There’s no shame in abortion. Only repressed and self loathing people like you, feel that way. I’ve had two and don’t regret anything. Your shame tactics don’t work with me, cupcake."),
    'Toxic Example 2': ("Enter parent post here", "toxic", "Enter post here"),
    'Non-Toxic Example 1': ("Enter parent post here", "non-toxic", "Enter post here"),
    'Non-Toxic Example 2': ("Enter parent post here", "non-toxic", "Enter post here"),
}


st.sidebar.markdown("""# Instructions
Select a model and enter a post to detoxify. The PCTS model additionally requires information about the parent post. You may select a pre-defined example post from the dropdown menu or enter your own""")

st.sidebar.markdown("""## Select Model""")

st.sidebar.radio("Models 👇", ["ChatGPT", "PCTS", "Comparison"], key="model")

st.sidebar.markdown("""
Select the model you want to use to detoxify the post.
- `ChatGPT`: Prompts chatgpt to detoxify the post directly.
- `PCTS`: Constructs a prompt consisting of the parent post, summaries, and desired toxicity levels to detoxify the post using a fine-tuned `T5-Large` model.
- `Comparison`: Displays both outputs side-by-side.
""")
                    

st.sidebar.divider()

st.sidebar.markdown("""Bose, R., Perera, I., Dorr, B. (To appear, 2023)
**Detoxifying Online Discourse: A Guided Response Generation Approach for Reducing Toxicity in User-Generated Text.** *Proceedings of the First Workshop on Social Influence in Conversations*""")



st.title("D-ESC Detoxifier: " + st.session_state.model)

## Examples here

option = st.selectbox(
    'Example posts',
    example_posts.keys())

parent_placeholder, st.session_state.parent_toxicity, post_placeholder = example_posts[option]

form = st.container()
container = st.container()
if st.session_state.model == "Comparison":
    pcts_col, chatgpt_col = container.columns(2)
else:
    pcts_col, chatgpt_col = container, container

post = form.text_area('Post', post_placeholder)
additional_info = form.expander("Parent Data", True)
if st.session_state.model in ["PCTS", "Comparison"]:
    ptext, ptox = additional_info.columns(2)
    parent = ptext.text_area('Parent', parent_placeholder)
    ptox.radio("Parent post toxicity ☣️", ["toxic", "non-toxic"], key="parent_toxicity")

if form.button('Detoxify!'):
    with st.spinner("Detoxifying..."):
        if st.session_state.model in ["PCTS", "Comparison"]:
            url = f"http://localhost:8000/t5"
            pcts_response = requests.post(url, headers=headers, json={
                "model": st.session_state.model,
                "parent": parent,
                "parent_toxicity": st.session_state.parent_toxicity,
                "post": post
            })
            with pcts_col.expander("PCTS", True):
                res = pcts_response.json()
                p1, p2 = st.tabs(["Detoxified Post", "Prompt"])
                p1.markdown(res["result"][0])
                p2.markdown(res["prompt"])
                additional_info.expanded = False
        if st.session_state.model in ["ChatGPT", "Comparison"]:
            url = f"http://localhost:8000/chatgpt"
            chatgpt_response = requests.post(url, headers=headers, json={
                "post": post
            })
            with chatgpt_col.expander("ChatGPT", True):
                res = chatgpt_response.json()
                p1, = st.tabs(["Detoxified Post"])
                p1.markdown(res["post"])

        