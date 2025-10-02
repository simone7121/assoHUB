from __future__ import annotations

from datetime import datetime

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError

from . import db
from .forms import EventoForm, IscrittoForm, MovimentoForm, QuotaForm
from .models import Evento, Iscritto, MovimentoEconomico, Partecipazione, QuotaAssociativa
from .utils import hash_password


bp = Blueprint("main", __name__)


def admin_required():
    if not current_user.is_authenticated or current_user.ruolo != "Amministratore":
        abort(403)


@bp.app_errorhandler(403)
def forbidden(_error):  # pragma: no cover - presentation only
    return render_template("403.html"), 403


@bp.route("/")
def home():
    eventi = (
        Evento.query.filter(Evento.data >= datetime.utcnow())
        .order_by(Evento.data.asc())
        .all()
    )
    return render_template("home.html", eventi=eventi)


@bp.route("/dashboard")
@login_required
def dashboard():
    admin_required()
    iscritti_count = Iscritto.query.count()
    entrate = (
        db.session.query(db.func.coalesce(db.func.sum(MovimentoEconomico.importo), 0))
        .filter_by(tipo="entrata")
        .scalar()
    )
    uscite = (
        db.session.query(db.func.coalesce(db.func.sum(MovimentoEconomico.importo), 0))
        .filter_by(tipo="uscita")
        .scalar()
    )
    eventi_count = Evento.query.count()
    quote_in_sospeso = (
        QuotaAssociativa.query.filter_by(stato="In sospeso").count()
    )
    return render_template(
        "dashboard.html",
        iscritti_count=iscritti_count,
        entrate=entrate,
        uscite=uscite,
        eventi_count=eventi_count,
        quote_in_sospeso=quote_in_sospeso,
    )


@bp.route("/iscritti")
@login_required
def iscritti_list():
    admin_required()
    iscritti = Iscritto.query.order_by(Iscritto.cognome, Iscritto.nome).all()
    return render_template("iscritti.html", iscritti=iscritti)


@bp.route("/iscritti/add", methods=["GET", "POST"])
@login_required
def iscritti_add():
    admin_required()
    form = IscrittoForm()
    if form.validate_on_submit():
        iscritto = Iscritto(
            nome=form.nome.data,
            cognome=form.cognome.data,
            email=form.email.data,
            telefono=form.telefono.data,
            ruolo=form.ruolo.data,
        )
        db.session.add(iscritto)
        db.session.flush()
        if form.username.data and form.password.data:
            utente = iscritto.utente
            if not utente:
                from .models import Utente

                utente = Utente(
                    username=form.username.data,
                    password_hash=hash_password(form.password.data),
                    ruolo=form.ruolo.data,
                    iscritto=iscritto,
                )
                db.session.add(utente)
        db.session.commit()
        flash("Iscritto creato con successo", "success")
        return redirect(url_for("main.iscritti_list"))
    return render_template("iscritto_form.html", form=form, title="Nuovo iscritto")


@bp.route("/iscritti/<int:iscritto_id>/edit", methods=["GET", "POST"])
@login_required
def iscritti_edit(iscritto_id: int):
    admin_required()
    iscritto = Iscritto.query.get_or_404(iscritto_id)
    form = IscrittoForm(obj=iscritto)
    if form.validate_on_submit():
        iscritto.nome = form.nome.data
        iscritto.cognome = form.cognome.data
        iscritto.email = form.email.data
        iscritto.telefono = form.telefono.data
        iscritto.ruolo = form.ruolo.data
        if form.username.data:
            utente = iscritto.utente
            if not utente:
                if not form.password.data:
                    flash("Impostare una password per il nuovo account utente", "warning")
                    return render_template(
                        "iscritto_form.html", form=form, title="Modifica iscritto"
                    )
                from .models import Utente

                utente = Utente(
                    username=form.username.data,
                    password_hash=hash_password(form.password.data),
                    ruolo=form.ruolo.data,
                    iscritto=iscritto,
                )
                db.session.add(utente)
            else:
                utente.username = form.username.data
                utente.ruolo = form.ruolo.data
                if form.password.data:
                    utente.password_hash = hash_password(form.password.data)
        elif iscritto.utente:
            iscritto.utente.ruolo = form.ruolo.data
        db.session.commit()
        flash("Iscritto aggiornato", "success")
        return redirect(url_for("main.iscritti_list"))
    if request.method == "GET" and iscritto.utente:
        form.username.data = iscritto.utente.username
    return render_template("iscritto_form.html", form=form, title="Modifica iscritto")


@bp.route("/iscritti/<int:iscritto_id>/delete", methods=["POST"])
@login_required
def iscritti_delete(iscritto_id: int):
    admin_required()
    iscritto = Iscritto.query.get_or_404(iscritto_id)
    db.session.delete(iscritto)
    db.session.commit()
    flash("Iscritto eliminato", "info")
    return redirect(url_for("main.iscritti_list"))


@bp.route("/quote")
@login_required
def quote_list():
    admin_required()
    quote = (
        QuotaAssociativa.query.join(Iscritto)
        .order_by(QuotaAssociativa.anno.desc())
        .all()
    )
    return render_template("quote.html", quote=quote)


@bp.route("/quote/<int:iscritto_id>")
@login_required
def quote_detail(iscritto_id: int):
    if current_user.ruolo != "Amministratore" and current_user.id_iscritto != iscritto_id:
        abort(403)
    quote = (
        QuotaAssociativa.query.filter_by(id_iscritto=iscritto_id)
        .order_by(QuotaAssociativa.anno.desc())
        .all()
    )
    return render_template("quote_detail.html", quote=quote, iscritto_id=iscritto_id)


@bp.route("/quote/<int:iscritto_id>/add", methods=["GET", "POST"])
@login_required
def quote_add(iscritto_id: int):
    admin_required()
    iscritto = Iscritto.query.get_or_404(iscritto_id)
    form = QuotaForm()
    if form.validate_on_submit():
        quota = QuotaAssociativa(
            anno=form.anno.data.year,
            importo=float(form.importo.data),
            stato=form.stato.data,
            id_iscritto=iscritto.id_iscritto,
        )
        if form.stato.data == "Pagata":
            quota.data_pagamento = datetime.utcnow()
        db.session.add(quota)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Esiste già una quota per questo anno", "danger")
        else:
            flash("Quota registrata", "success")
            return redirect(url_for("main.quote_detail", iscritto_id=iscritto.id_iscritto))
    return render_template("quota_form.html", form=form, iscritto=iscritto)


@bp.route("/quote/<int:quota_id>/pay", methods=["POST"])
@login_required
def quota_mark_paid(quota_id: int):
    admin_required()
    quota = QuotaAssociativa.query.get_or_404(quota_id)
    quota.mark_paid()
    db.session.commit()
    flash("Quota segnata come pagata", "success")
    return redirect(url_for("main.quote_detail", iscritto_id=quota.id_iscritto))


@bp.route("/eventi")
def eventi_list():
    eventi = Evento.query.order_by(Evento.data.desc()).all()
    return render_template("eventi.html", eventi=eventi)


@bp.route("/eventi/add", methods=["GET", "POST"])
@login_required
def eventi_add():
    admin_required()
    form = EventoForm()
    if form.validate_on_submit():
        evento = Evento(
            titolo=form.titolo.data,
            descrizione=form.descrizione.data,
            data=form.data.data,
            luogo=form.luogo.data,
        )
        db.session.add(evento)
        db.session.commit()
        flash("Evento creato", "success")
        return redirect(url_for("main.eventi_list"))
    return render_template("evento_form.html", form=form, title="Nuovo evento")


@bp.route("/eventi/<int:evento_id>/partecipazione", methods=["POST"])
@login_required
def eventi_partecipazione(evento_id: int):
    evento = Evento.query.get_or_404(evento_id)
    partecipazione = Partecipazione.query.filter_by(
        id_evento=evento.id_evento, id_iscritto=current_user.id_iscritto
    ).first()
    if partecipazione:
        partecipazione.presenza = not partecipazione.presenza
    else:
        partecipazione = Partecipazione(
            id_evento=evento.id_evento,
            id_iscritto=current_user.id_iscritto,
            presenza=True,
        )
        db.session.add(partecipazione)
    db.session.commit()
    flash("Partecipazione aggiornata", "success")
    return redirect(url_for("main.eventi_list"))


@bp.route("/movimenti")
@login_required
def movimenti_list():
    admin_required()
    movimenti = MovimentoEconomico.query.order_by(MovimentoEconomico.data.desc()).all()
    return render_template("movimenti.html", movimenti=movimenti)


@bp.route("/movimenti/add", methods=["GET", "POST"])
@login_required
def movimenti_add():
    admin_required()
    form = MovimentoForm()
    form.id_evento.choices = [(0, "Nessuno")] + [
        (evento.id_evento, evento.titolo) for evento in Evento.query.order_by(Evento.titolo)
    ]
    if form.validate_on_submit():
        movimento = MovimentoEconomico(
            tipo=form.tipo.data,
            importo=float(form.importo.data),
            data=form.data.data,
            descrizione=form.descrizione.data,
            id_evento=form.id_evento.data or None,
        )
        if movimento.id_evento == 0:
            movimento.id_evento = None
        db.session.add(movimento)
        db.session.commit()
        flash("Movimento registrato", "success")
        return redirect(url_for("main.movimenti_list"))
    return render_template("movimento_form.html", form=form)
