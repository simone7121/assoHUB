# AssoHUB

AssoHUB è una web app Django per la gestione completa di un'associazione: iscritti, quote associative, eventi, partecipazioni e movimenti economici.

## Requisiti

- Python 3.11+
- [pip](https://pip.pypa.io/en/stable/)

## Installazione

```bash
python -m venv .venv
source .venv/bin/activate
# AssoHUB

AssoHUB è una web app sviluppata con Django per gestire le attività di un'associazione: soci, quote associative, eventi, partecipazioni e movimenti economici.

Questa repository contiene il codice sorgente, la configurazione di base (SQLite) e le pagine template per una piccola associazione o per uso didattico.

## Sommario rapido

- Requisiti: Python 3.10+ (testato con 3.10/3.11), pip
- Database di default: SQLite (file `db.sqlite3` nella root)
- Ambiente virtuale consigliato: `.venv`
- Server di sviluppo: `python manage.py runserver`

## Requisiti

- Python 3.10+
- pip
- (opzionale) virtualenv

I pacchetti Python richiesti sono elencati in `requirements.txt`.

## Installazione e avvio (Windows - PowerShell)

1. Crea e attiva un ambiente virtuale:

```powershell
python -m venv .venv
# In PowerShell
.\.venv\Scripts\Activate.ps1
```

Se PowerShell blocca l'esecuzione degli script, puoi abilitare l'esecuzione per l'utente corrente:

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

4. Avvia il server di sviluppo (porta predefinita 8000):

```powershell
python manage.py runserver
```

Se preferisci un'altra porta o hai problemi di permessi, usa esplicitamente una porta libera, ad esempio 8080:

```powershell
python manage.py runserver 8080
```

Oppure fai il bind a localhost esplicito (utile se hai restrizioni di rete):

```powershell
python manage.py runserver 127.0.0.1:8000
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

- Il progetto usa per default `assohub/settings.py` con configurazioni adatte allo sviluppo (DEBUG=True). Non usare la stessa configurazione in produzione.
- Per deploy in produzione impostare una chiave sicura in `SECRET_KEY`, impostare `DEBUG=False`, configurare `ALLOWED_HOSTS` e usare un DB più robusto (Postgres/MySQL).
- Per servire file statici in produzione eseguire `python manage.py collectstatic` e configurare un server (nginx, etc.).

## Database

Per default il progetto usa SQLite (file `db.sqlite3`). Per cambiare database, aggiornare `assohub/settings.py` e installare il driver necessario.

## Test

Esegui i test con:

```powershell
python manage.py test
```

## Risoluzione problemi comuni

- "source .venv/bin/activate" non funziona su PowerShell: è un comando per shell Unix; su PowerShell usa `\\.venv\\Scripts\\Activate.ps1`.
- Errore "You don't have permission to access that port":
	- Verifica se la porta è occupata:

```powershell
netstat -ano | findstr :8000
```

	- Se trovi un PID che occupa la porta, termina il processo (sostituisci <PID>):

```powershell
taskkill /PID <PID> /F
```

	- Esegui il server su un'altra porta (es. 8080):

```powershell
python manage.py runserver 8080
```

	- Se il problema è di permessi di sistema, apri PowerShell come amministratore e riprova.

## Funzionalità principali

- Autenticazione e gestione utenti con ruoli (es. socio, amministratore)
- CRUD per i soci
- Gestione delle quote associative e stato pagamenti
- Eventi: creazione, elenco e iscrizioni
- Tracciamento delle partecipazioni agli eventi
- Movimenti economici (entrate/uscite) e dashboard con indicatori

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

Se vuoi contribuire:

1. Fork del repository
2. Crea un branch feature/bugfix
3. Aggiungi test quando possibile
4. Apri una pull request descrivendo il cambiamento

## Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi il file `LICENSE` per i dettagli.

## Contatti

Per domande o segnalazioni apri un issue o contatta l'autore tramite l'email presente nel repository.

---

File aggiornato automaticamente: fornisci feedback se vuoi aggiungere sezioni (es. setup Docker, deploy Heroku, integrazione CI/CD, ecc.).
