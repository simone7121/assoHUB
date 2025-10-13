from __future__ import annotations

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views
from .forms import LoginForm

urlpatterns = [
    path("login/", LoginView.as_view(authentication_form=LoginForm, template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profilo/", views.profile, name="profile"),
    path("", views.public_home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("iscritti/", views.members_list, name="members_list"),
    path("iscritti/add/", views.member_create, name="member_create"),
    path("iscritti/<int:pk>/edit/", views.member_update, name="member_update"),
    path("iscritti/<int:pk>/delete/", views.member_delete, name="member_delete"),
    path("quote/", views.fees_list, name="fees_list"),
    path("quote/add/", views.fees_manage, name="fees_create"),
    path("quote/<int:member_id>/", views.member_fees, name="member_fees"),
    path("eventi/", views.events_list, name="events_list"),
    path("eventi/add/", views.event_create, name="event_create"),
    path("eventi/<int:pk>/edit/", views.event_update, name="event_update"),
    path("eventi/<int:event_id>/iscriviti/", views.event_register, name="event_register"),
    path("eventi/<int:event_id>/partecipazioni/<int:pk>/", views.participation_update, name="participation_update"),
    path("movimenti/", views.transactions_list, name="transactions_list"),
    path("movimenti/add/", views.transaction_create, name="transaction_create"),
]
