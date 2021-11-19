from django.urls import path
from . import views

app_name = 'contact_form'
urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("contact", views.contact, name="contact"),
]
