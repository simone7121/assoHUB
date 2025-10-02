from __future__ import annotations

from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Event, FinancialTransaction, Member, MembershipFee, Participation, User


class BootstrapFormMixin:
    """Mixin per applicare classi Bootstrap ai campi."""

    def _apply_bootstrap(self):
        for field in self.fields.values():
            css_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"form-control {css_class}".strip()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class MemberForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Member
        fields = ["first_name", "last_name", "email", "phone", "role", "active"]


class MemberUserForm(MemberForm):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta(MemberForm.Meta):
        fields = MemberForm.Meta.fields

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError("Questo username è già in uso.")
        return username

    def save(self, commit=True):
        member = super().save(commit=commit)
        if commit:
            User.objects.create_user(
                username=self.cleaned_data["username"],
                password=self.cleaned_data["password"],
                member=member,
                role=member.role,
            )
        return member


class EventForm(BootstrapFormMixin, forms.ModelForm):
    date = forms.DateTimeField(
        label="Data e ora",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )

    class Meta:
        model = Event
        fields = ["title", "description", "date", "location"]


class MembershipFeeForm(BootstrapFormMixin, forms.ModelForm):
    payment_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = MembershipFee
        fields = ["member", "year", "amount", "payment_date", "status"]


class ParticipationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Participation
        fields = ["presence"]


class FinancialTransactionForm(BootstrapFormMixin, forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = FinancialTransaction
        fields = ["transaction_type", "amount", "date", "description", "event"]
