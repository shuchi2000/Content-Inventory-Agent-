import streamlit as st
from agent import agent,generate_prompt

# Set up the page layout
st.set_page_config(layout="wide")

# Store conversation in the session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Store conversation in the session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Function to display chat conversation in the main area
def display_conversation():
    for message in st.session_state.conversation:
        if message['role'] == "User":
            st.markdown(f"<div style='text-align:right; padding: 8px; background-color:#f1f1f1; border-radius:10px; margin-top:10px'>{message['text']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:left; padding: 8px; background-color:#e1e1e1; border-radius:10px; margin-top:10px'>{message['text']}</div>", unsafe_allow_html=True)

# Function to add message to conversation
def add_message(role, text):
    st.session_state.conversation.append({"role": role, "text": text})


# Left sidebar with the company logo, content creator's name, and select box
with st.sidebar:
    st.image(r"D:\my Github\Database-AI-Agent\Content Inventory Agent\logo.webp", width=150)  # Replace with actual path to your logo
    creator_name = st.selectbox(
        "Select Creator Name",('Ayushi Gupta', 'Shuchismita Mallick', 'Rohit Ganjoo',
       'Amit Choudhary', 'Mandar Sawant', 'Sai Somanadha Sastry Konduri',
       'Sayli Nikumbh', 'Divyanshi Sharan', 'Burhanuddin Nahargarwala',
       'Sourabh Kumar', 'Mansi Mutreja'))
    content_state = st.selectbox(
        "Select Content State",
        ("Draft", "Archived ", "Published")
    )
    # User input for chat
    user_input = st.text_input("Write your query", "")

    # Send button
    if st.button("Send"):
        if user_input:
            # Add user message to conversation
            add_message("User", user_input)

            # Generate improved prompt
            prompt = generate_prompt(user_input, creator_name, content_state)

            # Call the agent with the selected creator and status
            agent_instance = agent(creator_name, content_state)  # Get the agent
            if isinstance(agent_instance, str):
                # If agent returned an error message (string), display it
                add_message("Bot", agent_instance)
            else:
                # If agent is created successfully, run the prompt
                bot_response = agent_instance.run(prompt)
                add_message("Bot", bot_response)



# Main chat interface box
st.title("Content Inventory Support")
display_conversation()

