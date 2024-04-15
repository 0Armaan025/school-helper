import email
import os.path
import base64
import json
import re
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import logging
import requests


username = "Armaan Sir"
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.modify']

def readEmails():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                # your creds file here. Please create json file as here https://cloud.google.com/docs/authentication/getting-started
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages', [])
        if not messages:
            print('No new messages.')
        else:
            with open('email_subjects.txt', 'a', encoding='utf-8') as file:
                count = 0  # Counter to limit to 30 mails
                for message in messages:
                    if count >= 30:
                        break  # Break out of the loop if 30 mails are processed
                    msg = service.users().messages().get(userId='me', id=message['id']).execute()
                    email_data = msg['payload']['headers']
                    for values in email_data:
                        name = values['name']
                        if name == 'Subject':
                            subject = values['value']
                            file.write(f"{subject}\n")  # Write subject to file
                            count += 1  # Increment the counter
                            # Optionally, mark the message as read
                            msg = service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()
    except Exception as error:
        print(f'An error occurred: {error}')


options = ["1.) Check last 10 mails", "2.) Check Activity on discord , mention server name."]

def startup():

    print(f"Hello {username}, What do you want to do today?")

    for option in options:
        print(option)

    choice = int(input())    

def main():
    readEmails()

if __name__ == "__main__":
    main()