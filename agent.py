import os
from langchain_experimental.agents import create_csv_agent
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

# Initialize the LLM
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

creator = "Ayushi Gupta"
status = "Published"
# Base path for organized CSV files
output_base_path = r"D:\my Github\Database-AI-Agent\Content Inventory Agent\data"

def select_file(creator,status):

    # Convert creator name to folder name format
    creator_folder_name = creator.split(' ')[0] + "_" + creator.split(' ')[1]

    # Construct the path to the CSV file
    creator_folder_path = os.path.join(output_base_path, creator_folder_name)
    file_name = f"{status.upper()}.csv"
    file_path = os.path.join(creator_folder_path, file_name)
    return file_path

def agent(creator, status):
    # Get the file path
    file_path = select_file(creator, status)
    
    # Check if the file exists
    if os.path.exists(file_path):
        # File exists, create the agent
        agent = create_csv_agent(llm=llm, path=file_path, verbose=True, allow_dangerous_code=True, handle_parsing_errors=True)
        return agent
    else:
        # File does not exist, return an error message
        return "Sorry, We don't have any information regarding this."



def generate_prompt(user_query, creator, status):
    """
    This function generates an improved prompt by including additional context like content state and creator's name.
    """
    prompt_template = f"""
    Creator: {creator}
    Content State: {status}
    User Query: {user_query}

    Please provide in a report format- a detailed and accurate response based on the above information.
    Must contain in the report format: 
    1. Content Name 
    2. Content ID
    3. Tags to input percent
    """
    return prompt_template 