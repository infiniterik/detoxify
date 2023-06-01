import streamlit as st
import requests

st.set_page_config(page_title="Preliminary: D-ESC Stance-driven post generation", page_icon="☣️", layout="wide")

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)

if "api_key" not in st.session_state:
    st.session_state["api_key"]="my-secret"

headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": f"Bearer {st.session_state.api_key}"
}

if "stances" not in st.session_state:
        st.session_state.stances = []

sample_stances = {
    "<CHOOSE(woman)3.0,1.0>": "A strong belief a woman's right to choose and a positive sentiment towards a woman's right to choose.",
    "<CONTROL(woman)3.0,-1.0>": "A strong belief that a woman's body is being controlled by a third party and negative sentiment towards the control of a woman's body by a third party.",
    "<KILL_CHILD[kill[children]],3.00,-1>": "Strong belief that children are being killed and a negative sentiment towards the killing of children.",
    "<BAN_ABORTION[ban[abortion]],2.50,1>": "Somewhat strong belief that abortion should be banned and a positive sentiment towards banning abortions."
}

st.sidebar.markdown("""# Instructions
Select stances to be expressed in a single post. The post will be generated using GPT3.5 and then smoothed by the T5 model.
""")


st.title("Preliminary: D-ESC Stance-driven post generation")

st.multiselect("stances", sample_stances.keys(), key="stances")
stances = " ".join([sample_stances[s] for s in st.session_state.stances])
strep = "\n* ".join([f"{s}: {sample_stances[s]}" for s in st.session_state.stances])
if st.session_state.stances:
      st.markdown(f"## Stances:\n* {strep}")


if st.button('Generate!'):
    with st.spinner("Generate..."):
        url = f"http://localhost:8000/stanceDriven"
        generated_post = requests.post(url, headers=headers, json={"stances": stances})
        with st.expander("Stances", True):
                res = generated_post.json()
                #st.write(res["prompt"])
                cgpt = res["prompt"].split("Reply summary:")[1].split("A low toxicity reply:")[0].strip()
                p1, p2, p3 = st.tabs(["D-ESC Smoothed Post", "GPT3.5 Response", "Prompt"])
                p1.markdown(res["result"][0])
                p2.markdown(cgpt)
                p3.markdown(res["prompt"])