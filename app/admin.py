from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import Event, FinancialTransaction, Member, MembershipFee, Participation, User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = DjangoUserAdmin.fieldsets + (("Ruolo", {"fields": ("role", "member")}),)
    list_display = ("username", "email", "role", "member")
    list_filter = ("role",)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "role", "active")
    search_fields = ("first_name", "last_name", "email")
    list_filter = ("role", "active")


@admin.register(MembershipFee)
class MembershipFeeAdmin(admin.ModelAdmin):
    list_display = ("member", "year", "amount", "status", "payment_date")
    list_filter = ("status", "year")
    search_fields = ("member__first_name", "member__last_name")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "location")
    list_filter = ("date",)
    search_fields = ("title", "location")


@admin.register(Participation)
class ParticipationAdmin(admin.ModelAdmin):
    list_display = ("event", "member", "presence", "registered_at")
    list_filter = ("presence", "event")


@admin.register(FinancialTransaction)
class FinancialTransactionAdmin(admin.ModelAdmin):
    list_display = ("transaction_type", "amount", "date", "event")
    list_filter = ("transaction_type", "date")
    search_fields = ("description",)
