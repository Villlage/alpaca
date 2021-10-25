import re
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from bs4 import BeautifulSoup
import base64
from app import logger

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def parse_stocks_email_to_stocks_v1(text:str):
    stocks = []  
    all_stocks_text = re.findall('\nCheck out the following new tickers:(.*)', text)
    texstush = all_stocks_text[0][1:].strip().split(', ')
    for stock_text in texstush:
        text_with_stock_name = stock_text.split(' ')[0].split(':')[1]
        stocks.append(text_with_stock_name)
    return stocks


def parse_stocks_email_to_stocks_v2(text:str):
    stocks = []  
    # looking for where to start and grab the stocks from
    text_with_stock_info = re.findall('Check out the following new tickers:(.*)', text)

    # taking the stock names
    stocks_text = re.findall(r'break-word;">(.*?)<', text_with_stock_info[1])

    # going over the stock names and extracing them from the text
    for stock_text in stocks_text:
        stock_name = stock_text.split(' ')[0].split(':')[1]
        stocks.append(stock_name)
    return stocks


def parse_stocks_email_to_stocks(text:str):
    stocks1 = []
    stocks2 = []

    try:
        stocks1 = parse_stocks_email_to_stocks_v1(text)
    except Exception as error:
        logger.debug(error)

    try:
        stocks2 = parse_stocks_email_to_stocks_v2(text)
    except Exception as error:
        logger.debug(error)

    if stocks1:
        return stocks1
    elif stocks2:
        return stocks2
    else:
        logger.error(f"no text was found {text}")
        return []
    



def _get_sender(headers):
    # get email subject    
    # Look for Subject and Sender Email in the headers
    for d in headers:
        if d['name'] == 'From':
            return d['value']


def _get_email_data(message):
    try:
        # Get the message from its id
        text = service.users().messages().get(userId='me', id=message['id']).execute()
        # Get value of 'payload' from dictionary 'text'
        payload = text['payload']
        sender = _get_sender(payload['headers'])
        # decode data
        if payload.get('parts'):
            data = payload.get('parts')[0]['body']['data']
        else:
            data = payload['body']['data']

        data = data.replace("-","+").replace("_","/")
        decoded_data = base64.b64decode(data)
        decoded_data_utf = decoded_data.decode("utf-8")

    except Exception as error:
        logger.debug(error)
        raise Exception(error)

    return decoded_data_utf, sender


def get_emails(messages):
    decoded_data_arr = []
    for message in messages:
        email_data, _ = _get_email_data(message)
        decoded_data_arr.append(email_data)

    return decoded_data_arr
  

def get_stocks_data():
    """
    getting data from the first email that was just sent
    """
    result = service.users().messages().list(userId='me').execute()
    messages = result.get('messages')
    email_text, sender = _get_email_data(messages[0])
    # if not "tradingview" in sender:
    #     return [] 
    stocks = parse_stocks_email_to_stocks(email_text)
    return stocks


def get_service():
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    return service

service = get_service()



# def watch_deal():
    # get_labels()

    # request = {'labelIds': ['INBOX'],'topicName': 'projects/aerial-resolver-329812/topics/gmail-api'}
    # service.users().watch(userId='me', body=request).execute()

    # result = service.users().messages().list(userId='me').execute()
    # messages = result.get('messages')
    # get_emails(messages, service)
