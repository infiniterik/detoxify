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


api_key = st.sidebar.text_input('Enter API KEY here', "my-secret", key="api_key")
is_local = st.sidebar.checkbox("Local", key="local")
base_url = "http://localhost:8000"
if not is_local:
    base_url = st.sidebar.text_input('Enter API KEY here', "http://localhost:8000", key="base-url")

