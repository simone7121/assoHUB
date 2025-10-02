from __future__ import annotations

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from .forms import LoginForm
from .models import Utente
from .utils import verify_password


bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = Utente.query.filter_by(username=form.username.data).first()
        if user and verify_password(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Accesso effettuato", "success")
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            if user.ruolo == "Amministratore":
                return redirect(url_for("main.dashboard"))
            return redirect(url_for("main.home"))
        flash("Credenziali non valide", "danger")
    return render_template("login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logout effettuato", "info")
    return redirect(url_for("auth.login"))
