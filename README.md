[![AssoHUB banner](Docs/AssoHubBanner.png)](https://github.com/simone7121/AssoHub/blob/main/Docs/AssoHubBanner.png?raw=true)

# AssoHUB

AssoHUB è una web app Django per la gestione completa di un'associazione: soci, quote associative, eventi, partecipazioni e movimenti economici.

## Requisiti

- Python 3.10+ (consigliato 3.11)
- pip
- (opzionale) virtualenv

I pacchetti richiesti sono elencati in `requirements.txt`.

## Installazione e avvio (Windows - PowerShell)

1. Crea e attiva un ambiente virtuale:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Se PowerShell blocca l'esecuzione degli script:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\.venv\Scripts\Activate.ps1
```

2. Installa le dipendenze:

```powershell
pip install -r requirements.txt
```

3. Applica le migrazioni e crea l'utente amministratore:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

4. Avvia il server di sviluppo:

```powershell
python manage.py runserver
# oppure specifica porta/host
python manage.py runserver 127.0.0.1:8000
python manage.py runserver 8080
```

## Installazione e avvio (macOS / Linux - bash/zsh)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Configurazione per lo sviluppo

- Il progetto usa `assohub/settings.py` con DEBUG=True per lo sviluppo.
- Non usare la stessa configurazione in produzione: impostare `SECRET_KEY`, `DEBUG=False` e configurare `ALLOWED_HOSTS`.
- Per la produzione usare un DB più robusto (Postgres/MySQL) e servire i file statici con `collectstatic` + server (nginx, etc.).

## Database

Per default usa SQLite (file `db.sqlite3` nella root). Per cambiare DB, aggiornare `assohub/settings.py` e installare il driver necessario.

## Test

Esegui i test con:

```powershell
python manage.py test
```

## Risoluzione problemi comuni

- "source .venv/bin/activate" non funziona su PowerShell: è per shell Unix; usa `\.venv\Scripts\Activate.ps1`.
- Porta 8000 occupata:

```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
# oppure avvia il server su un'altra porta:
python manage.py runserver 8080
```

## Funzionalità principali

- Autenticazione e gestione utenti con ruoli (socio, amministratore)
- CRUD per i soci
- Gestione quote associative e stato pagamenti
- Eventi: creazione, elenco e iscrizioni
- Tracciamento partecipazioni agli eventi
- Movimenti economici (entrate/uscite) e dashboard

## Struttura del progetto

```
AssoHUB/
├── app/                 # app Django principale (models, views, templates)
│   ├── migrations/
│   ├── static/
│   └── templates/
├── assohub/             # configurazione Django del progetto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py/asgi.py
├── db.sqlite3            # database SQLite (opzionale, creato dopo migrate)
├── manage.py
├── requirements.txt
└── README.md
```

## Contributi

1. Fork del repository
2. Crea un branch feature/bugfix
3. Aggiungi test quando possibile
4. Apri una pull request descrivendo i cambiamenti

## Licenza

Distribuito sotto licenza MIT. Vedi il file `LICENSE`.

## Contatti

Per domande o segnalazioni apri un issue o contatta l'autore via email (vedi info nel repository).