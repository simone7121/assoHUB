from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from flask_login import UserMixin
from sqlalchemy import UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import db, login_manager


class Iscritto(db.Model):
    __tablename__ = "iscritti"

    id_iscritto: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(db.String(120), nullable=False)
    cognome: Mapped[str] = mapped_column(db.String(120), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(db.String(50))
    ruolo: Mapped[str] = mapped_column(db.String(50), default="Associato", nullable=False)

    utente: Mapped["Utente"] = relationship(back_populates="iscritto", uselist=False)
    quote: Mapped[list["QuotaAssociativa"]] = relationship(
        back_populates="iscritto", cascade="all, delete-orphan"
    )
    partecipazioni: Mapped[list["Partecipazione"]] = relationship(
        back_populates="iscritto", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Iscritto {self.nome} {self.cognome}>"


class QuotaAssociativa(db.Model):
    __tablename__ = "quote_associative"
    __table_args__ = (UniqueConstraint("anno", "id_iscritto", name="uq_quota_iscritto"),)

    id_quota: Mapped[int] = mapped_column(primary_key=True)
    anno: Mapped[int] = mapped_column(nullable=False)
    importo: Mapped[float] = mapped_column(db.Float(asdecimal=True), nullable=False)
    data_pagamento: Mapped[Optional[datetime]] = mapped_column(db.DateTime)
    stato: Mapped[str] = mapped_column(db.String(20), default="In sospeso", nullable=False)
    id_iscritto: Mapped[int] = mapped_column(db.ForeignKey("iscritti.id_iscritto"), nullable=False)

    iscritto: Mapped[Iscritto] = relationship(back_populates="quote")

    def mark_paid(self) -> None:
        self.stato = "Pagata"
        self.data_pagamento = datetime.utcnow()


class Evento(db.Model):
    __tablename__ = "eventi"

    id_evento: Mapped[int] = mapped_column(primary_key=True)
    titolo: Mapped[str] = mapped_column(db.String(200), nullable=False)
    descrizione: Mapped[Optional[str]] = mapped_column(db.Text)
    data: Mapped[datetime] = mapped_column(nullable=False)
    luogo: Mapped[str] = mapped_column(db.String(200), nullable=False)

    partecipazioni: Mapped[list["Partecipazione"]] = relationship(
        back_populates="evento", cascade="all, delete-orphan"
    )
    movimenti: Mapped[list["MovimentoEconomico"]] = relationship(
        back_populates="evento", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Evento {self.titolo} ({self.data:%Y-%m-%d})>"


class Partecipazione(db.Model):
    __tablename__ = "partecipazioni"
    __table_args__ = (
        UniqueConstraint("id_iscritto", "id_evento", name="uq_iscritto_evento"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    id_iscritto: Mapped[int] = mapped_column(db.ForeignKey("iscritti.id_iscritto"), nullable=False)
    id_evento: Mapped[int] = mapped_column(db.ForeignKey("eventi.id_evento"), nullable=False)
    presenza: Mapped[bool] = mapped_column(default=False, nullable=False)

    iscritto: Mapped[Iscritto] = relationship(back_populates="partecipazioni")
    evento: Mapped[Evento] = relationship(back_populates="partecipazioni")


class MovimentoEconomico(db.Model):
    __tablename__ = "movimenti_economici"
    __table_args__ = (
        CheckConstraint("tipo IN ('entrata', 'uscita')", name="ck_tipo_movimento"),
    )

    id_movimento: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[str] = mapped_column(db.String(10), nullable=False)
    importo: Mapped[float] = mapped_column(db.Float(asdecimal=True), nullable=False)
    data: Mapped[date] = mapped_column(db.Date, default=date.today, nullable=False)
    descrizione: Mapped[Optional[str]] = mapped_column(db.Text)
    id_evento: Mapped[Optional[int]] = mapped_column(db.ForeignKey("eventi.id_evento"))

    evento: Mapped[Optional[Evento]] = relationship(back_populates="movimenti")


class Utente(UserMixin, db.Model):
    __tablename__ = "utenti"

    id_utente: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(80), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(db.String(255), nullable=False)
    ruolo: Mapped[str] = mapped_column(db.String(50), nullable=False)
    id_iscritto: Mapped[int] = mapped_column(db.ForeignKey("iscritti.id_iscritto"), unique=True)

    iscritto: Mapped[Iscritto] = relationship(back_populates="utente")

    def get_id(self) -> str:
        return str(self.id_utente)


@login_manager.user_loader
def load_user(user_id: str) -> Optional[Utente]:  # pragma: no cover - simple proxy
    return db.session.get(Utente, int(user_id))
