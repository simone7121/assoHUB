from __future__ import annotations

from datetime import date, datetime

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    DateTimeLocalField,
    DecimalField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=80)])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Ricordami")
    submit = SubmitField("Accedi")


class IscrittoForm(FlaskForm):
    nome = StringField("Nome", validators=[DataRequired(), Length(max=120)])
    cognome = StringField("Cognome", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    telefono = StringField("Telefono", validators=[Optional(), Length(max=50)])
    ruolo = SelectField(
        "Ruolo",
        choices=[("Associato", "Associato"), ("Amministratore", "Amministratore")],
        validators=[DataRequired()],
    )
    username = StringField("Username", validators=[Optional(), Length(max=80)])
    password = PasswordField("Password", validators=[Optional(), Length(min=6)])
    submit = SubmitField("Salva")


class EventoForm(FlaskForm):
    titolo = StringField("Titolo", validators=[DataRequired(), Length(max=200)])
    descrizione = TextAreaField("Descrizione", validators=[Optional()])
    data = DateTimeLocalField(
        "Data",
        validators=[DataRequired()],
        default=datetime.utcnow,
        format="%Y-%m-%dT%H:%M",
    )
    luogo = StringField("Luogo", validators=[DataRequired(), Length(max=200)])
    submit = SubmitField("Salva")


class QuotaForm(FlaskForm):
    anno = DateField("Anno", format="%Y-%m-%d", validators=[DataRequired()])
    importo = DecimalField(
        "Importo", validators=[DataRequired(), NumberRange(min=0)], places=2
    )
    stato = SelectField(
        "Stato",
        choices=[("In sospeso", "In sospeso"), ("Pagata", "Pagata")],
        validators=[DataRequired()],
    )
    submit = SubmitField("Registra")


class MovimentoForm(FlaskForm):
    tipo = SelectField(
        "Tipo",
        choices=[("entrata", "Entrata"), ("uscita", "Uscita")],
        validators=[DataRequired()],
    )
    importo = DecimalField(
        "Importo", validators=[DataRequired(), NumberRange(min=0)], places=2
    )
    data = DateField("Data", validators=[DataRequired()], default=date.today)
    descrizione = TextAreaField("Descrizione", validators=[Optional()])
    id_evento = SelectField("Evento", coerce=int, validators=[Optional()])
    submit = SubmitField("Salva")
