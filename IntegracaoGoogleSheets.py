from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1Wiuoh1Pj9zqqLNfE57HOvGTObeuFdimCIztsMqncpns'
SAMPLE_RANGE_NAME = 'Página1!A1:D10'


def main():
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
                'credential.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Inicializar o Google Sheets
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Adicionar/editar informações do Google Sheets
        valores_adicionar = [
            ['Diamantes', '500.000', 'Dólar'],
            ['Bitcoins', '100.000', 'Dólar'],
        ]
        result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range='A9', valueInputOption='USER_ENTERED', body={'values': valores_adicionar}).execute()

        # Ler informaçõesdo Google Sheets
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        valores = result['values']
        print(valores)

        # Adicionar/editar informações do Google Sheets
        impostos_adicionar = [
            ['Imposto'],
        ]
        for i, linha in enumerate(valores):
            if i > 0:
                precos = linha[1]
                precos = precos.replace('.', '')
                precos = float(precos.replace(',', '.'))
                imposto = precos * 0.1
                impostos_adicionar.append([imposto])

        result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range='D1', valueInputOption='USER_ENTERED', body={'values': impostos_adicionar}).execute()

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()