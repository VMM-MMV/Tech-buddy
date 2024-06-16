import streamlit_survey as ss
import streamlit as st
from webscout import PhindSearch
import pages.util.laptops as laptops

# Create an instance of the PHIND class
ph = PhindSearch()

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


survey = ss.StreamlitSurvey()

survey.multiselect("What would be your primary use of your computer?", options=["Gaming", "Work", "School", "Day to day living"])

survey.multiselect("What is important to you?", options=["Portability", "Battery Life", "Storage Size", "Screen Size"])

survey.multiselect("Additional Features?", options=["HDMI Port", "Screen Resolution", "Keyboard Backlight"])

if st.button('Click me'):
    print(survey.to_json())
    response = ph.ask(user_prompt+"Explain the difference in specification between these computers, do not just list the specs for every model, instead compare their values for each category I am a complete beginner explain in detail. DO NOT USE TECHNICAL JARGON, YOUR TASK IS TO EXPLAIN EACH COMPUTER COMPONENT AND HOW THEY DIFFER FROM MODEL TO MODEL"+laptops.get_laptops(str(survey.to_json())))
    final=ph.get_message(response).split("@$")[-1]
    print(final)
    st.title(final)