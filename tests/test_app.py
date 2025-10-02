import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import create_app, db
from app.models import Iscritto, Utente
from app.utils import hash_password
from config import TestConfig


@pytest.fixture()
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def test_create_iscritto_and_user(app):
    with app.app_context():
        iscritto = Iscritto(
            nome="Mario",
            cognome="Rossi",
            email="mario@example.com",
            ruolo="Amministratore",
        )
        db.session.add(iscritto)
        db.session.flush()
        utente = Utente(
            username="mario",
            password_hash=hash_password("password123"),
            ruolo="Amministratore",
            iscritto=iscritto,
        )
        db.session.add(utente)
        db.session.commit()

        assert Utente.query.count() == 1
        assert Utente.query.first().iscritto.email == "mario@example.com"


def test_homepage_accessible(client):
    response = client.get("/")
    assert response.status_code == 200
