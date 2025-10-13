from __future__ import annotations

from datetime import datetime

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    EventForm,
    FinancialTransactionForm,
    MemberForm,
    MemberUserForm,
    MembershipFeeForm,
    ParticipationForm,
    PasswordAggiornamentoForm,
    UserProfileForm,
)
from .models import Event, FinancialTransaction, Member, MembershipFee, Participation
from .utils import admin_required


def public_home(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by("date")
    participations = []
    if request.user.is_authenticated and hasattr(request.user, "member"):
        participations = Participation.objects.filter(
            member=request.user.member, event__in=upcoming_events
        ).values_list("event_id", flat=True)
    return render(
        request,
        "home.html",
        {
            "events": upcoming_events,
            "participations": participations,
        },
    )


@login_required
def profile(request):
    user = request.user
    if request.method == "POST":
        if "profile_submit" in request.POST:
            profile_form = UserProfileForm(request.POST, user=user)
            password_form = PasswordAggiornamentoForm(user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profilo aggiornato con successo.")
                return redirect("profile")
        elif "password_submit" in request.POST:
            profile_form = UserProfileForm(user=user)
            password_form = PasswordAggiornamentoForm(user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, "Password aggiornata correttamente.")
                return redirect("profile")
        else:
            profile_form = UserProfileForm(user=user)
            password_form = PasswordAggiornamentoForm(user)
    else:
        profile_form = UserProfileForm(user=user)
        password_form = PasswordAggiornamentoForm(user)
    return render(
        request,
        "account/profile.html",
        {
            "profile_form": profile_form,
            "password_form": password_form,
        },
    )


@admin_required
def dashboard(request):
    members_count = Member.objects.filter(active=True).count()
    events_count = Event.objects.count()
    income_total = (
        FinancialTransaction.objects.filter(transaction_type=FinancialTransaction.TYPE_ENTRATA)
        .aggregate(total=Sum("amount"))
        .get("total")
        or 0
    )
    expense_total = (
        FinancialTransaction.objects.filter(transaction_type=FinancialTransaction.TYPE_USCITA)
        .aggregate(total=Sum("amount"))
        .get("total")
        or 0
    )
    balance = income_total - expense_total
    recent_events = Event.objects.order_by("-date")[:5]
    fees_status = (
        MembershipFee.objects.values("status")
        .annotate(total=Count("id"))
        .order_by("status")
    )

    context = {
        "members_count": members_count,
        "events_count": events_count,
        "income_total": income_total,
        "expense_total": expense_total,
        "balance": balance,
        "recent_events": recent_events,
        "fees_status": fees_status,
    }
    return render(request, "dashboard.html", context)


@admin_required
def members_list(request):
    members = Member.objects.all()
    return render(request, "members/list.html", {"members": members})


@admin_required
def member_create(request):
    if request.method == "POST":
        form = MemberUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Iscritto creato con successo.")
            return redirect("members_list")
    else:
        form = MemberUserForm()
    return render(request, "members/form.html", {"form": form, "title": "Nuovo iscritto"})


@admin_required
def member_update(request, pk: int):
    member = get_object_or_404(Member, pk=pk)
    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            member = form.save()
            if hasattr(member, "user"):
                member.user.role = member.role
                member.user.save(update_fields=["role"])
            messages.success(request, "Iscritto aggiornato correttamente.")
            return redirect("members_list")
    else:
        form = MemberForm(instance=member)
    return render(request, "members/form.html", {"form": form, "title": "Modifica iscritto"})


@admin_required
def member_delete(request, pk: int):
    member = get_object_or_404(Member, pk=pk)
    if request.method == "POST":
        member.delete()
        messages.success(request, "Iscritto eliminato.")
        return redirect("members_list")
    return render(request, "members/confirm_delete.html", {"member": member})


@login_required
def fees_list(request):
    if getattr(request.user, "is_administrator", False):
        fees = MembershipFee.objects.select_related("member")
    else:
        fees = MembershipFee.objects.filter(member=request.user.member)
    return render(request, "fees/list.html", {"fees": fees})


@login_required
def member_fees(request, member_id: int):
    member = get_object_or_404(Member, pk=member_id)
    if request.user.is_associate and request.user.member != member:
        messages.error(request, "Non puoi visualizzare le quote di altri associati.")
        return redirect("fees_list")
    fees = member.fees.all().order_by("-year")
    return render(request, "fees/detail.html", {"member": member, "fees": fees})


def events_list(request):
    now = timezone.now()
    future_events = Event.objects.filter(date__gte=now).order_by("date")
    past_events = Event.objects.filter(date__lt=now).order_by("-date")[:5]
    user_participations = []
    if hasattr(request.user, "member"):
        user_participations = Participation.objects.filter(member=request.user.member).values_list(
            "event_id", flat=True
        )
    context = {
        "future_events": future_events,
        "past_events": past_events,
        "user_participations": user_participations,
    }
    return render(request, "events/list.html", context)


@admin_required
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Evento creato correttamente.")
            return redirect("events_list")
    else:
        form = EventForm(initial={"date": datetime.now().strftime("%Y-%m-%dT18:00")})
    return render(request, "events/form.html", {"form": form, "title": "Nuovo evento"})


@admin_required
def event_update(request, pk: int):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Evento aggiornato correttamente.")
            return redirect("events_list")
    else:
        form = EventForm(instance=event)
    return render(request, "events/form.html", {"form": form, "title": "Modifica evento"})


@login_required
def event_register(request, event_id: int):
    event = get_object_or_404(Event, pk=event_id)
    try:
        member = request.user.member
    except Member.DoesNotExist:
        messages.error(request, "Solo gli iscritti possono registrarsi agli eventi.")
        return redirect("events_list")
    participation, created = Participation.objects.get_or_create(member=member, event=event)
    if created:
        messages.success(request, "Iscrizione all'evento registrata.")
    else:
        messages.info(request, "Sei gia iscritto a questo evento.")
    return redirect("events_list")


@admin_required
def participation_update(request, event_id: int, pk: int):
    participation = get_object_or_404(Participation, pk=pk, event_id=event_id)
    if request.method == "POST":
        form = ParticipationForm(request.POST, instance=participation)
        if form.is_valid():
            form.save()
            messages.success(request, "Partecipazione aggiornata.")
            return redirect("events_list")
    else:
        form = ParticipationForm(instance=participation)
    return render(
        request,
        "events/participation_form.html",
        {"form": form, "title": "Aggiorna partecipazione", "participation": participation},
    )


@admin_required
def transactions_list(request):
    transactions = FinancialTransaction.objects.select_related("event")
    total_income = transactions.filter(transaction_type=FinancialTransaction.TYPE_ENTRATA).aggregate(
        total=Sum("amount")
    )["total"] or 0
    total_expense = transactions.filter(transaction_type=FinancialTransaction.TYPE_USCITA).aggregate(
        total=Sum("amount")
    )["total"] or 0
    balance = total_income - total_expense
    return render(
        request,
        "transactions/list.html",
        {
            "transactions": transactions,
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance,
        },
    )


@admin_required
def transaction_create(request):
    if request.method == "POST":
        form = FinancialTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Movimento registrato correttamente.")
            return redirect("transactions_list")
    else:
        form = FinancialTransactionForm(initial={"date": datetime.now().date()})
    return render(request, "transactions/form.html", {"form": form, "title": "Nuovo movimento"})


@admin_required
def fees_manage(request):
    if request.method == "POST":
        form = MembershipFeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Quota registrata correttamente.")
            return redirect("fees_list")
    else:
        form = MembershipFeeForm()
    return render(request, "fees/form.html", {"form": form, "title": "Nuova quota"})
