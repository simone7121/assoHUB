from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


def current_year() -> int:
    return timezone.now().year


class Member(models.Model):
    ROLE_ASSOCIATO = "associato"
    ROLE_AMMINISTRATORE = "amministratore"
    ROLE_CHOICES = [
        (ROLE_ASSOCIATO, "Associato"),
        (ROLE_AMMINISTRATORE, "Amministratore"),
    ]

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_ASSOCIATO)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        return f"{self.full_name}"

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()


class User(AbstractUser):
    ROLE_ASSOCIATO = Member.ROLE_ASSOCIATO
    ROLE_AMMINISTRATORE = Member.ROLE_AMMINISTRATORE
    ROLE_CHOICES = Member.ROLE_CHOICES

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_ASSOCIATO)
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name="user", blank=True, null=True)

    def save(self, *args, **kwargs):
        if self._state.adding and not type(self).objects.exists():  # first user defaults to admin
            self.role = self.ROLE_AMMINISTRATORE
        if self.member_id:
            try:
                member = self.member
            except Member.DoesNotExist:  # user can exist without linked member
                member = None
            if member and member.role != self.role:
                member.role = self.role
                member.save(update_fields=["role"])
        super().save(*args, **kwargs)

    @property
    def is_associate(self) -> bool:
        return self.role == self.ROLE_ASSOCIATO

    @property
    def is_administrator(self) -> bool:
        return self.role == self.ROLE_AMMINISTRATORE

    @property
    def display_name(self) -> str:
        try:
            member = self.member
        except Member.DoesNotExist:
            member = None
        if member and member.full_name:
            return member.full_name
        full_name = self.get_full_name()
        return full_name or self.username


    @property
    def has_member(self) -> bool:
        if not self.member_id:
            return False
        try:
            self.member
        except Member.DoesNotExist:
            return False
        return True


class MembershipFee(models.Model):
    STATUS_PAGATO = "pagato"
    STATUS_PENDENTE = "pendente"
    STATUS_CHOICES = [
        (STATUS_PENDENTE, "Pendente"),
        (STATUS_PAGATO, "Pagato"),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="fees")
    year = models.PositiveIntegerField(default=current_year)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_PENDENTE)

    class Meta:
        verbose_name = "Quota associativa"
        verbose_name_plural = "Quote associative"
        constraints = [
            models.UniqueConstraint(fields=["member", "year"], name="unique_fee_per_member_year"),
        ]
        ordering = ["-year", "member__last_name"]

    def __str__(self) -> str:
        return f"Quota {self.year} - {self.member.full_name}"


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)

    class Meta:
        ordering = ["date"]

    def __str__(self) -> str:
        return self.title

    @property
    def is_future(self) -> bool:
        return self.date >= timezone.now()


class Participation(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="participations")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="participations")
    presence = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["member", "event"], name="unique_participation"),
        ]
        ordering = ["event__date"]

    def __str__(self) -> str:
        return f"{self.member.full_name} - {self.event.title}"


class FinancialTransaction(models.Model):
    TYPE_ENTRATA = "entrata"
    TYPE_USCITA = "uscita"
    TYPE_CHOICES = [
        (TYPE_ENTRATA, "Entrata"),
        (TYPE_USCITA, "Uscita"),
    ]

    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=255)
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.SET_NULL, related_name="transactions")

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self) -> str:
        return f"{self.get_transaction_type_display()} - {self.amount} €"

    @property
    def signed_amount(self) -> float:
        return float(self.amount if self.transaction_type == self.TYPE_ENTRATA else -self.amount)
