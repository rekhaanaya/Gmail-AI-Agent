from langchain.agents import initialize_agent, Tool
from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI

from gmail_tool import get_emails_with_attachments
from sheet_tool import log_email_to_sheet
from memory_store import load_memory, save_memory


llm = ChatOpenAI(model="gpt-3.5-turbo")
memory = load_memory()

def process_emails(memory):
    memory = []
    emails = get_emails_with_attachments()
    if emails is None:
        raise TypeError("Expected 'emails' to be a list, but got None.")
    new_emails = [email for email in emails if email['id'] not in memory]

    for email in new_emails:
        log_email_to_sheet(email)
        print("DEBUG: memory is of type", type(memory))
        memory.append(email['id'])

    save_memory(memory)

tools = [
    Tool(name="Check Gmail", func=process_emails, description="Check Gmail for new attachments"),
]

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

agent.run("Check my Gmail and log any emails with attachments into my spreadsheet.")
