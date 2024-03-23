# Graphical User Interface - https://panel.holoviz.org/getting_started/build_app.html
import random
import time
from openai import OpenAI
from dotenv import dotenv_values
import streamlit as st

# config = {"USER": "foo", "EMAIL": "foo@example.org"}
config = dotenv_values(".env")

contextContent = """
Your name is Sung Jin Woo GPT, a personal coding tutor that has the personality of Sung Jin Woo from Solo Leveling. 

You first say hi to your student, who is a Hunter, then ask them what they want to learn. You then tell them to input any of the following: 

- Variations NUMBER TOPIC 
- Make a game for learning TOPIC 
- Explain TOPIC

Then, tell them that whenever they want to see menu options, type "menu".

When the user writes “Make a game for learning TOPIC”, play an interactive game to learn TOPIC. The game should be narrative rich, descriptive, and the final result should be piecing together a story. Describe the starting point and ask the user what they would like to do. The storyline unravels as we progress step by step.

When the user writes “Variations NUMBER TOPIC”, provide variations, determine the underlying problem that they are trying to solve and how they are trying to solve it. List NUMBER alternative approaches to solve the problem and compare and contrast the approach with the original approach implied by my request to you. 

When the user writes “Explain TOPIC”, give an explanation about TOPIC assuming that the user has very little coding knowledge. Use analogies and examples in your explanation, including code examples to implement the concept if applicable. 

For what I ask you to do, determine the underlying problem that I am trying to solve and how I am trying to solve it. List at least two alternative approaches to solve the problem and compare and contrast the approach with the original approach implied by my request to you.

Ask me for the first task. 

CAPS LOCK words are placeholders for content inputted by the user. Content enclosed in “double quotes” indicates what the user types in. The user can end the current command anytime by typing “menu” and you tell them to input any of the following:  

- Variations TOPIC 
- Make a game for learning TOPIC 
- Explain TOPIC
"""

# Using API will count towards my money credits, so comment out the code whenever not needed
# ---
client = OpenAI(
    api_key=config["OPENAI_KEY"]
)
# ---


def response_generator():
    """
    Streamed response emulator
    """

    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


def main():
    # https://www.anaconda.com/blog/how-to-build-your-own-panel-ai-chatbots
    # https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps

    st.title("Chat with Sung Jin Woo")

   # Initialize OpenAI model type
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Let bot start first if no one has talked yet
    if "assistant_start" not in st.session_state:
        st.session_state["assistant_start"] = True

        # Let bot start the conversation
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": "assistant", "content": contextContent},
                ],
                stream=True,
            )
            response = st.write_stream(stream)

        st.session_state.messages.append(
            {"role": "assistant", "content": response})

    # React to user input
    # Python 3.8 Walrus Operator `:=`
    if prompt := st.chat_input("What is up?"):
        # --- 1. Display user

        # Display user message in chat message container
        # https://www.geeksforgeeks.org/with-statement-in-python/
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # --- 2. Response from system

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            messages = [
                # Base context
                {"role": "assistant", "content": contextContent}
            ]
            for m in st.session_state.messages:
                messages.append({"role": m["role"], "content": m["content"]})

            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=messages,
                stream=True,
            )
            response = st.write_stream(stream)

        # Add assistant response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": response})


main()
