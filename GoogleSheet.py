import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_to_googlesheet():
    """
    Connette l'applicazione al foglio di lavoro su Google Drive.
    :param sheet_name: Nome del foglio di lavoro.
    :param credentials_file: Percorso del file di credenziali.
    :return: Oggetto worksheet per il foglio di lavoro specificato.
    """

    # Scopes delle API di Google Drive
    scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # Credenziali dell'applicazione
    creds = ServiceAccountCredentials.from_json_keyfile_name('client.json', scopes)

    # Autorizzazione dell'applicazione
    client = gspread.authorize(creds)

    # Apertura del foglio di lavoro
    sheet = client.open('KANBAN')
    wk = sheet.worksheet('Kanban')
    wc = sheet.worksheet('Clean')
    # Bloccare la prima riga del foglio di lavoro di destinazione
    headerK = wk.row_values(1)
    wk.freeze(rows=1)
    # Bloccare la prima riga del foglio di lavoro di destinazione
    headerC = wc.row_values(1)
    wc.freeze(rows=1)
    # Restituzione dell'oggetto worksheet
    return sheet