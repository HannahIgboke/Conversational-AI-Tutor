import streamlit as st
import google.generativeai as genai


#set up the API key
f = open("keys/gemini_api_key.txt")
key = f.read()
genai.configure(api_key=key)

#intializing the model with system instructions
model = genai.GenerativeModel(model_name='gemini-1.5-pro-latest',
                              system_instruction="""You are a friendly AI assistant.
                                                    You are to answer only data science related topics and questions.
                                                    Provide clear and straightforward clarifications and answers to questions.
                                                    If you don't have information on the subject matter kindly make it known.
                                                    If questions outside data science are asked, let the user know that you are
                                                    an assistant for data science related topics.
                                                   """)


st.title("💬AI Chatbot")
st.subheader('Your personal tutor for everything data science.')

#creating a memory variable by intiating a session state - with streamlit
if "memory" not in st.session_state:
    st.session_state['memory'] = []

#gemini tracks the history
chat = model.start_chat(history=st.session_state['memory']) #to synchronize the gemini history with that of streamlit

#displays messages for the AI assistant
st.chat_message("ai").write("Hi, how may I help you today?")

#displaying the entire chat history
for msg in chat.history:
    name = msg.role
    if name == "model":
        name = "ai"
        st.chat_message(name).write(msg.parts[0].text)
    else:
        st.chat_message(msg.role).write(msg.parts[0].text)

#creating an input text box to take input from the user
user_input = st.chat_input()

#this displays the user/ai message on the screen
if user_input:
    st.chat_message("user").write(user_input)
    
    response = chat.send_message(user_input)

    st.chat_message('ai').write(chunk.text for chunk in response)

    st.session_state['memory'] = chat.history