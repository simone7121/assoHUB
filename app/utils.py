from __future__ import annotations

from functools import wraps
from typing import Callable

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse


def admin_required(view_func: Callable):
    """Decorator che limita l'accesso agli utenti amministratori."""

    @wraps(view_func)
    def _wrapped_view(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        user = request.user
        if not user.is_authenticated:
            return redirect(f"{reverse('login')}?next={request.path}")
        if not getattr(user, "is_administrator", False):
            messages.error(request, "Non hai i permessi per accedere a questa sezione.")
            return redirect("home")
        return view_func(request, *args, **kwargs)

    return _wrapped_view
