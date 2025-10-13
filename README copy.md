# AssoHUB

AssoHUB è una web app Django per la gestione completa di un'associazione: iscritti, quote associative, eventi, partecipazioni e movimenti economici.

## Requisiti

- Python 3.11+
- [pip](https://pip.pypa.io/en/stable/)

## Installazione

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configurazione

Le impostazioni predefinite usano SQLite come database locale e una chiave `SECRET_KEY` di sviluppo. Per l'uso in produzione personalizzare `assohub/settings.py` con valori sicuri e un database adeguato.

## Migrazioni database

```bash
python manage.py migrate
```

## Creazione superutente

```bash
python manage.py createsuperuser
```

## Avvio server di sviluppo

```bash
python manage.py runserver
```

L'applicazione sarà disponibile su [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Funzionalità principali

- Autenticazione con ruoli (Associato e Amministratore del direttivo)
- Gestione iscritti (CRUD) e creazione automatica delle credenziali
- Registro delle quote associative e stato pagamenti
- Calendario eventi, iscrizione dei soci e tracciamento presenze
- Movimenti economici (entrate/uscite) con saldo
- Dashboard amministrativa con indicatori chiave

## Struttura del progetto

```
assoHUB/
├── app/
│   ├── admin.py
│   ├── forms.py
│   ├── migrations/
│   ├── models.py
│   ├── templates/
│   ├── static/
│   ├── urls.py
│   └── views.py
├── assohub/
│   ├── settings.py
│   └── urls.py
├── manage.py
├── requirements.txt
└── README.md
```

## Test

I test possono essere eseguiti con:

```bash
python manage.py test
```

## Licenza

Distribuito sotto licenza MIT. Vedi il file [LICENSE](LICENSE) per ulteriori dettagli.
