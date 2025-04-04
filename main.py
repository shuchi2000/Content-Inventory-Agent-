import streamlit as st
import os
import pandas as pd
from langchain_experimental.agents import create_csv_agent
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

# Initialize the LLM
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# Base path for organized CSV files
output_base_path = r"D:\my Github\Database-AI-Agent\content_inventory_agent\data"

# Streamlit app setup
st.title("Content Inventory Support")

# Session state to store creator name, content status, and chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'creator_name' not in st.session_state:
    st.session_state.creator_name = None
if 'content_status' not in st.session_state:
    st.session_state.content_status = None

# Ask for creator's name if not provided
if st.session_state.creator_name is None:
    with st.form("creator_form"):
        creator_name = st.text_input("Please enter your name:", "")
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.session_state.creator_name = creator_name

# Once creator's name is provided, proceed with content status selection
if st.session_state.creator_name is not None:
    with st.form("status_form"):
        content_status = st.selectbox("Select content status:", ["ARCHIVED", "DRAFT", "PUBLISHED"])
        submitted_status = st.form_submit_button("Submit Status")
        if submitted_status:
            st.session_state.content_status = content_status

    # Find the appropriate CSV file based on creator name and content status
    if st.session_state.content_status is not None:
        st.write(f"Welcome, {st.session_state.creator_name}!")
        st.write(f"Content Status: {st.session_state.content_status}")

        # Extract the first name from the input
        first_name = st.session_state.creator_name.split(" ")[0]

        # Convert creator name to folder name format
        creator_folder_name = first_name + "_" + st.session_state.creator_name.split(" ")[1] if len(st.session_state.creator_name.split(" ")) > 1 else first_name

        # Construct the path to the CSV file
        creator_folder_path = os.path.join(output_base_path, creator_folder_name)
        file_name = f"{st.session_state.content_status}.csv"
        file_path = os.path.join(creator_folder_path, file_name)

        # Check if the file exists
        if os.path.exists(file_path):
            # Create LangChain agent with the selected CSV file
            agent = create_csv_agent(llm=llm, path=file_path, verbose=True,allow_dangerous_code=True,handle_parsing_errors=True)

            # Chat interface
            with st.form("query_form"):
                query = st.text_input("Ask a question about the data:", "")
                submitted_query = st.form_submit_button("Submit")

                if submitted_query:
                    try:
                        # Run the query through the agent
                        response = agent.run(query)
                        st.write("Response:", response)

                        # Store chat history
                        st.session_state.chat_history.append({
                            "query": query,
                            "response": response,
                            "status": st.session_state.content_status,
                            "creator": st.session_state.creator_name
                        })

                    except Exception as e:
                        st.error(f"Error occurred: {str(e)}")

            # Display chat history
            if len(st.session_state.chat_history) > 0:
                st.write("Chat History:")
                for i, entry in enumerate(st.session_state.chat_history):
                    st.write(f"**Query {i+1}**: {entry['query']}")
                    st.write(f"**Response**: {entry['response']}")
                    st.write(f"**Status**: {entry['status']}, **Creator**: {entry['creator']}\n")

            # Save chat history to CSV
            if st.button("Save Chat History"):
                history_df = pd.DataFrame(st.session_state.chat_history)
                history_df.to_csv("chat_history.csv", index=False)
                st.success("Chat history saved to chat_history.csv")
        else:
            st.error(f"CSV file not found for {st.session_state.creator_name} with status {st.session_state.content_status}.")
