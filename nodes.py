import os
import time

from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.search import GmailSearch

class Nodes():
    def __init__(self):
        self.gmail = GmailToolkit()

    def check_gmail(self, state):
        print("Checking Gmail inbox for new emails...")
        # Ensure the Gmail API is initialized
        search = GmailSearch(api_resource=self.gmail.api_resource)
        emails = search('after:newer_than:1d')  # Fetch emails from the last day
        # Filter out already checked emails
        checked_emails = state.get('checked_emails_ids', [])

        thread = []
        new_emails = []
        print(f"Found {len(emails)} emails in the last day.\n")
        print("Here are the new emails:", emails)
        # Filter out emails from the current user
        for email in emails:
            # Check if the email is not already checked and not from the current user
            if (email['id'] not in checked_emails and (email['threadID'] not in thread) and (os.environ['MY_EMAIL'] not in email['sender'])):
                thread.append(email['threadID']) # Track threads to avoid duplicates
                new_emails.append({
                    "id": email['id'],
                    "threadID": email['threadID'],
                    "snippet": email['snippet'],
                    "sender": email['sender']
                }) # Collect new emails
        checked_emails.extend([email['id'] for email in new_emails]) # Update checked emails
        return {
            # Double star means it expands what is in the state dictionary
            **state,  # Include existing state
            "emails": new_emails,  # Add new emails to the state
            "checked_emails_ids": checked_emails  # Update checked emails in the state
        }

    # This function is used to wait for the next run of the agent
    def wait_next_run(self, state):
        print("Waiting for 10 seconds...")
        time.sleep(10)
        return state

    # This function is used to check if there are new emails and return the appropriate state
    def new_gmails(self, state):
        if len(state['emails']) == 0:
            print("No new emails found!")
            return "end"
        else:
            print("New emails")
            return "continue"