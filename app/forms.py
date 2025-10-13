from __future__ import annotations

from typing import List

from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

from .models import Event, FinancialTransaction, Member, MembershipFee, Participation, User


class BootstrapFormMixin:
    """Mixin per applicare classi Bootstrap ai campi."""

    def _apply_bootstrap(self) -> None:
        for field in self.fields.values():
            css_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"form-control {css_class}".strip()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._apply_bootstrap()


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    error_messages = {
        "invalid_login": "Credenziali non valide. Controlla nome utente e password.",
        "inactive": "Questo account e' disattivato.",
    }

    username = forms.CharField(
        label="Nome utente",
        widget=forms.TextInput(attrs={"autofocus": True, "placeholder": "Nome utente"}),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )


class MemberForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Member
        fields = ["first_name", "last_name", "email", "phone", "role", "active"]
        labels = {
            "first_name": "Nome",
            "last_name": "Cognome",
            "email": "Email",
            "phone": "Telefono",
            "role": "Ruolo",
            "active": "Attivo",
        }


class MemberUserForm(MemberForm):
    username = forms.CharField(label="Nome utente")
    password = forms.CharField(label="Password iniziale", widget=forms.PasswordInput)

    class Meta(MemberForm.Meta):
        fields = MemberForm.Meta.fields

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError("Questo nome utente e' gia' in uso.")
        return username

    def save(self, commit: bool = True) -> Member:
        member = super().save(commit=commit)
        if commit:
            User.objects.create_user(
                username=self.cleaned_data["username"],
                password=self.cleaned_data["password"],
                member=member,
                role=member.role,
                email=member.email,
                first_name=member.first_name,
                last_name=member.last_name,
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
        labels = {
            "title": "Titolo",
            "description": "Descrizione",
            "location": "Luogo",
        }


class MembershipFeeForm(BootstrapFormMixin, forms.ModelForm):
    payment_date = forms.DateField(
        label="Data di pagamento",
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = MembershipFee
        fields = ["member", "year", "amount", "payment_date", "status"]
        labels = {
            "member": "Iscritto",
            "year": "Anno",
            "amount": "Importo",
            "status": "Stato",
        }


class ParticipationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Participation
        fields = ["presence"]
        labels = {
            "presence": "Presenza confermata",
        }


class FinancialTransactionForm(BootstrapFormMixin, forms.ModelForm):
    date = forms.DateField(
        label="Data",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    class Meta:
        model = FinancialTransaction
        fields = ["transaction_type", "amount", "date", "description", "event"]
        labels = {
            "transaction_type": "Tipo movimento",
            "amount": "Importo",
            "description": "Descrizione",
            "event": "Evento collegato",
        }


class UserProfileForm(BootstrapFormMixin, forms.Form):
    username = forms.CharField(label="Nome utente", max_length=150)
    first_name = forms.CharField(label="Nome", max_length=150)
    last_name = forms.CharField(label="Cognome", max_length=150)
    email = forms.EmailField(label="Email")
    phone = forms.CharField(label="Telefono", max_length=30, required=False)

    def __init__(self, *args, user: User, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self._member = None
        try:
            self._member = user.member
        except Member.DoesNotExist:
            self._member = None
        self.fields["username"].initial = user.username
        self.fields["first_name"].initial = user.first_name
        self.fields["last_name"].initial = user.last_name
        self.fields["email"].initial = user.email
        if self._member:
            self.fields["first_name"].initial = self._member.first_name
            self.fields["last_name"].initial = self._member.last_name
            self.fields["email"].initial = self._member.email
            self.fields["phone"].initial = self._member.phone
        else:
            self.fields.pop("phone")

    def clean_username(self) -> str:
        username = self.cleaned_data["username"]
        if User.objects.exclude(pk=self.user.pk).filter(username=username).exists():
            raise forms.ValidationError("Questo nome utente e' gia' in uso.")
        return username

    def clean_email(self) -> str:
        email = self.cleaned_data["email"]
        if self._member and Member.objects.exclude(pk=self._member.pk).filter(email=email).exists():
            raise forms.ValidationError("Questo indirizzo email e' gia' associato a un altro iscritto.")
        return email

    def save(self) -> User:
        user = self.user
        user.username = self.cleaned_data["username"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.save(update_fields=["username", "first_name", "last_name", "email"])

        if self._member:
            self._member.first_name = self.cleaned_data["first_name"]
            self._member.last_name = self.cleaned_data["last_name"]
            self._member.email = self.cleaned_data["email"]
            phone = self.cleaned_data.get("phone")
            if phone is not None:
                self._member.phone = phone
            update_fields: List[str] = ["first_name", "last_name", "email"]
            if "phone" in self.cleaned_data:
                update_fields.append("phone")
            self._member.save(update_fields=update_fields)
        return user


class PasswordAggiornamentoForm(BootstrapFormMixin, PasswordChangeForm):
    error_messages = {
        "password_incorrect": "La password attuale non e' corretta.",
        "password_mismatch": "Le nuove password non coincidono.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].label = "Password attuale"
        self.fields["new_password1"].label = "Nuova password"
        self.fields["new_password2"].label = "Conferma nuova password"
        for field in self.fields.values():
            field.widget.attrs.setdefault("placeholder", field.label)
