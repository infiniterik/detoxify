import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Civil Sanctuary - D-ESC Demo")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    **👈 Select a demo from the sidebar** to see some examples
    of D-ESC's Generative AI models!
    ### Want to learn more?
    Check out our paper in SICon in July 2023!
"""
)

if "api_key" not in st.session_state:
    st.session_state["api_key"]="my-secret"

api_key = st.text_input('API_KEY', "entry api key here", key="api_key")