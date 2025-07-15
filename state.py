import datetime
from typing import TypedDict

class EmailState(TypedDict):
    checked_emails_ids: list[str]  # List of email IDs that have been checked
    emails: list[dict]  # List of new emails with their details
    action_required_emails: dict # Dictionary to hold emails that require action 