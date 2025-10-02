# AssoHUB

AssoHUB è un sistema informativo web realizzato con Flask per la gestione completa di un'associazione. Permette di amministrare iscritti, eventi, quote associative, movimenti economici e prevede l'autenticazione degli utenti con ruoli differenziati.

## Funzionalità principali

- **Autenticazione** con ruoli _Associato_ e _Amministratore_.
- **Gestione iscritti** con CRUD completo e associazione 1-1 con gli utenti che accedono alla piattaforma.
- **Gestione eventi** con registrazione delle partecipazioni dei soci.
- **Gestione quote associative** con stato dei pagamenti per anno.
- **Gestione movimenti economici** (entrate/uscite) con eventuale collegamento agli eventi.
- **Dashboard amministrativa** con indicatori rapidi.

## Avvio progetto

1. Creare un ambiente virtuale e installare le dipendenze:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Esportare le variabili d'ambiente necessarie (facoltativo):

   ```bash
   export FLASK_APP=run.py
   export FLASK_ENV=development
   ```

3. Inizializzare il database e le migrazioni (opzionale):

   ```bash
   flask db init
   flask db migrate -m "Initial tables"
   flask db upgrade
   ```

4. Avviare l'applicazione:

   ```bash
   flask run
   ```

5. Eseguire i test:

   ```bash
   pytest
   ```

## Struttura del progetto

La struttura del progetto segue un'architettura modulare con blueprints, form e template organizzati secondo le funzionalità richieste.
