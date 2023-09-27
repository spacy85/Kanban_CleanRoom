# Kanban_CleanRoom

Descrizione:

Questo progetto è un'applicazione desktop sviluppata in Python utilizzando il framework PyQt5. L'applicazione offre un sistema di gestione dei componenti tra due aree chiave di produzione: la "Cleanroom" e il "Reparto Lavaggio". L'obiettivo principale è semplificare il processo di richiesta, lavaggio e monitoraggio dei componenti all'interno di un'azienda.

Funzionalità chiave:

Richiesta Componenti Cleanroom: Gli operatori nella "Cleanroom" possono inserire i codici dei componenti che necessitano di essere lavati. Queste richieste vengono inviate al "Reparto Lavaggio" per il trattamento.

Monitoraggio Stato Componenti: Gli operatori possono monitorare lo stato dei componenti in tempo reale. Lo stato può essere "In lavaggio", "In asciugatura" o "Pronti per il passbox". Queste informazioni sono visualizzate in una tabella interattiva.

Controllo da Passbox: Il "Passbox" è una stazione di controllo dove i componenti lavati vengono controllati prima di essere inviati indietro alla "Cleanroom". Gli operatori possono inserire il codice del componente per verificarne lo stato e autorizzare il rientro in Cleanroom.

Integrazione con Google Drive: I dati relativi ai componenti e alle richieste vengono memorizzati su Google Drive in fogli di calcolo. L'applicazione utilizza la libreria gspread per l'accesso e la modifica dei dati.

Tecnologie Utilizzate:

Python
PyQt5 (interfaccia utente)
gspread (accesso a Google Drive)
Google Sheets (per la memorizzazione dei dati)
Google Drive API (per l'accesso ai file su Google Drive)
Accesso Utente:

L'applicazione gestisce tre tipi di accesso:

Cleanroom: Gli operatori nella Cleanroom possono inviare richieste e monitorare lo stato dei componenti.
Lavaggio: Il personale del Reparto Lavaggio può visualizzare le richieste in arrivo, lavare i componenti e aggiornare lo stato.
Ospite: Un accesso limitato per la visualizzazione dello stato dei componenti senza la possibilità di inviare richieste.
