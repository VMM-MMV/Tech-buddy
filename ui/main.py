import streamlit as st
from pages.util.DarkMode import *
import pages.AI
theme_path=""".streamlit/config.toml"""

st.set_page_config(
    page_title="QuickSearch",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded",
)


def get_step():
    return st.session_state.get('step', 1)

def next_step():
    st.session_state['step'] = get_step() + 1

def write():


    app = FeatureActivator()

    app.run()

    st.write("# QuickFinder Demo")
    with open(theme_path,"r") as theme:
        data=theme.readlines()
        mode=data[2].replace(" ","")[:-2].split("\"")[-1]

        if mode=="light":
            st.title("You are in Normal Mode, check out Dark Mode!")
        else:
            st.title("You are in Dark Mode, New your searches are on 999.md")

    st.write("""Use Cases:
             \n1) You can ask a question, and the AI will respond to your question.
             \n2) To ensure you get the most affordable laptop, try taking a quiz.""")


st.button("Next", on_click=next_step)

if __name__ == "__main__":
    write()
