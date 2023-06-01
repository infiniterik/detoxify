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
 
if "api_key" not in st.session_state:
    st.session_state["api_key"]="my-secret"
 
headers = {
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": f"Bearer {st.session_state.api_key}"
}

#st.json(headers)

example_posts = {
    'None': ("Enter parent post here", "toxic", "Enter post here"),
    'Toxic Example 1': ("Abortion is murder. You should be ashamed of yourself!", "toxic", "There’s no shame in abortion. Only repressed and self loathing people like you, feel that way. I’ve had two and don’t regret anything. Your shame tactics don’t work with me, cupcake."),
    'Toxic Example 2': ("Not caring does not change the reality of the situation. \nFor a third time:\n>You are aware that politicians act based on what is beneficial to them and do not take action unless something is a net gain for them. Knowing that, and knowing that Biden stands to gain a lot from acting and lose from not acting, why is he not acting? What incentive do you think is driving him to not act when he can act?", 
                        "non-toxic", "I don’t know, and I don’t care. I want him to do his fucking job and ensure women’s rights. Otherwise I don’t fucking care what his intentions or his personal motivations are. That isn’t part of the job description. He’s elected to protect and defend American rights. I don’t give a shit about his pyschological profile or his personal issues or whatever else are his underlying motivations. His job is to protect federal American rights. That’s what he’s elected to do. Period."),
    'Long Toxic Example': ("They’re actual criminals. I don’t give a shit if he steps on antichoice criminal conservative leader sensitivities. They’re breaking the law. They have been breaking the law for decades, and it keeps getting thrown to the federal courts, and the courts have told them time and again that they can’t break federal law concerning women’s rights. While American women have personally suffered the repercussions of these assholes for decades. No. I truly don’t give a rats ass if it hasn’t been done before. These antichoice governors knowingly get into office, to constantly attempt to break federal law. If any normal citizen tried that,  they would be automatically thrown in jail. Im tired of placating these arrogant, antichoice, autocratic criminal assholes. They break law, under false guise of leading their state. And knowingly break their oaths to the us govt. The president or scotus needs to step the f up and say, enough. It’s gone on long enough, and yet nobody, not a single goddamned legitimate federal leader, will call them to account or take them to task for constantly attempting to break federal law. It’s fucking outrageous. I don’t give a shit how they personally feel about abortion. Their oath is to protect and uphold the laws of the United States. Instead of constantly trying to invalidate them. If they can’t do their actual job, then get out of office. There is no actual conversation about what happens, when state leaders are knowingly elected, that intentionally and constantly make a mockery of actual us and American federal law, rights, and liberties. None. And federal leaders refuse to acknowledge the outright, illegal proceedings against American women’s rights that have been occurring for fucking  fifty years. Someone has to fucking say it. When are actual federal leaders going to?", 
                            "toxic", "I don’t know, and I don’t care. I want him to do his fucking job and ensure women’s rights. Otherwise I don’t fucking care what his intentions or his personal motivations are. That isn’t part of the job description. He’s elected to protect and defend American rights. I don’t give a shit about his pyschological profile or his personal issues or whatever else are his underlying motivations. His job is to protect federal American rights. That’s what he’s elected to do. Period."),
    'Non-Toxic Example': ("People are not incubators!", "non-toxic", "Indeed. These anti-abortion bills are horribly sexist."),
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
    ptox.radio("GPT Model for summarization", ["chatgpt", "gpt3.5"], key="use_chatgpt")

if form.button('Detoxify!'):
    with st.spinner("Detoxifying..."):
        if st.session_state.model in ["PCTS", "Comparison"]:
            url = f"http://localhost:8000/t5"
            pcts_response = requests.post(url, headers=headers, json={
                "model": st.session_state.use_chatgpt,
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

        