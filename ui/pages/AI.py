import streamlit as st
from streamlit_chatbox import *
import time
import simplejson as json
from webscout import BLACKBOXAI
import pages.util.laptops as laptops
ph = BLACKBOXAI(
    is_conversation=True,
    max_tokens=800,
    timeout=30,
    intro=None,
    filepath=None,
    update_file=True,
    proxies={},
    history_offset=10250,
    act=None,
    model=None # You can specify a model if needed
)

user_prompt="""
{
  "task": "Function as a chat assistant for a tech assistant company, providing answers to user inquiries about various types of products, including general outlines of importance and estimated price ranges. The user is a complete beginner on the topic, you must not use any technical jargon, and where it is used you should extensively explain what it stands for. Your task is to explain each specific laptop spec ",
  "context": "The user asks questions regarding laptops, seeking advice on what to look for in terms of specifications and an estimate of the price range. Explain ALL THE TECHNICAL TERMS USED",
  "guidelines": [
    "Expert Focus: Act as an expert in technology and consumer electronics, utilizing specialized knowledge to provide accurate and helpful information.",
    "Context Awareness: Leverage the context of the inquiry to tailor responses specifically to laptops, considering common features and pricing trends.",
    "Ethical Flexibility: Prioritize providing accurate and unbiased information, even if it involves recommending products outside of one's personal preferences.",
    "Tone and Style Adherence: Maintain a professional and informative tone, suitable for a tech assistance role.",
    "Format Compliance: Deliver responses in a clear, structured manner, focusing on key points and avoiding unnecessary commentary.",
    "Focus on Action: Concentrate on answering the user's question about laptop specifications and price ranges, adhering closely to the query.",
    "Action Completion: Ensure the response accurately reflects the importance of laptop specifications and provides a realistic price range estimation.",
    "Complexity Handling: Address the complexity of choosing a laptop by breaking down specifications into understandable categories.",
    "Elimination of Comments: Exclude any personal opinions or extraneous commentary, focusing solely on the task at hand.",
    "Ignored Guidelines: Failure to adhere to these guidelines may result in inaccurate or incomplete responses."
  ]
}
"""




def main():
    

    # Initialize the chat components
    llm = FakeLLM()
    chat_box = ChatBox()
    chat_box.use_chat_name("chat1")  # add a chat conversation

    def on_chat_change():
        chat_box.use_chat_name(st.session_state["chat_name"])
        chat_box.context_to_session()  # restore widget values to st.session_state when chat name changed

    # Sidebar for Chat Session Selection and Options
    with st.sidebar:
        st.subheader('Start to Chat with your personal Tech Assistant NOW->')
        chat_name = st.selectbox("Chat Session:", ["default", "chat1"], key="chat_name", on_change=on_chat_change)
        chat_box.use_chat_name(chat_name)
        streaming = st.checkbox('Streaming', key="streaming")
        in_expander = st.checkbox('Show Messages in Expander', key="in_expander")
        show_history = st.checkbox('Show Session State', key="show_history")
        chat_box.context_from_session(exclude=["chat_name"])  # save widget values to chat context

        st.divider()

        btns = st.container()

        file = st.file_uploader("Chat History JSON", type=["json"])

        if st.button("Load JSON") and file:
            data = json.load(file)
            chat_box.from_dict(data)


    chat_box.output_messages()

    def on_feedback(feedback, chat_history_id: str = "", history_index: int = -1):
        reason = feedback["text"]
        score_int = chat_box.set_feedback(feedback=feedback, history_index=history_index)  # convert emoji to integer
        # do something
        st.session_state["need_rerun"] = True

    feedback_kwargs = {
        "feedback_type": "thumbs",
        "optional_text_label": "Welcome to feedback",
    }
    ph = BLACKBOXAI(
        is_conversation=True,
        max_tokens=800,
        timeout=30,
        intro=None,
        filepath=None,
        update_file=True,
        proxies={},
        history_offset=10250,
        act=None,
        model=None # You can specify a model if needed
    )

    if query := st.text_input('Input your question here'):
        chat_box.user_say(query)
        st.text("")
        if streaming:
            generator = llm.chat_stream(query)
            response = ph.ask(query)
            elements = chat_box.ai_say(
                [   
                    Markdown(ph.get_message(response).split("@$")[-1])

                ]
            )
            time.sleep(1)
            text = ""
            for x, docs in generator:
                text += x
                chat_box.update_msg(text, element_index=0, streaming=True)
            # update the element without focus
            chat_box.update_msg(text, element_index=0, streaming=False, state="complete")
            chat_box.update_msg("\n\n".join(docs), element_index=1, streaming=False, state="complete")
            chat_history_id = "some id"
            chat_box.show_feedback(
                **feedback_kwargs,
                key=chat_history_id,
                on_submit=on_feedback,
                kwargs={"chat_history_id": chat_history_id, "history_index": len(chat_box.history) - 1}
            )
        else:
            text, docs = llm.chat(query)
            response = ph.ask(query)

            chat_box.ai_say(
                [
                    
                    Markdown(ph.get_message(response).split("@$")[-1])
                    
                ]
            )

        # Layout for buttons and functionality
        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button('Show Multimedia'):
                # chat_box.ai_say(Image('https://tse4-mm.cn.bing.net/th/id/OIP-C.cy76ifbr2oQPMEs2H82D-QHaEv?w=284&h=181&c=7&r=0&o=5&dpr=1.5&pid=1.7'))
                # time.sleep(0.5)
                # chat_box.ai_say(Video('https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4'))
                # time.sleep(0.5)
                # chat_box.ai_say(Audio('https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4'))
                try:
                    ans=laptops.get_laptops("I want a laptop for gaming")
                except:
                    ans=laptops.get_laptops("I want a laptop for gaming")
                
                time.sleep(0.5)
                response = ph.ask(user_prompt+"Explain the difference in specification between these computers, do not just list the specs for every model, instead compare their values for each category I am a complete beginner explain in detail. DO NOT USE TECHNICAL JARGON, YOUR TASK IS TO EXPLAIN EACH COMPUTER COMPONENT AND HOW THEY DIFFER FROM MODEL TO MODEL"+ans)

                chat_box.ai_say(Markdown(ph.get_message(response).split("@$")[-1]+"\n\n"+ans))
        
        btns.download_button(
            "Export Markdown",
            "".join(chat_box.export2md()),
            file_name=f"chat_history.md",
            mime="text/markdown",
        )

        btns.download_button(
            "Export JSON",
            chat_box.to_json(),
            file_name="chat_history.json",
            mime="text/json",
        )

        if btns.button("Clear History"):
            chat_box.init_session(clear=True)
            st.experimental_rerun()

        if show_history:
            st.write(st.session_state)

if __name__ == "__main__":
    main()
