from django.shortcuts import render, redirect

from django_diplom.settings import EMAIL_HOST_USER
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse


def homepage(request):
    return render(request, "catalog/home.html")


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Пробное сообщение"
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],

            }
            recepient=body['email']
            message = "\n".join(body.values())
            try:
                send_mail(subject, message,
                          EMAIL_HOST_USER,
                          [EMAIL_HOST_USER])
            except BadHeaderError:
                return HttpResponse('Найден некорректный заголовок')
            return redirect("catalog:home")

    form = ContactForm()
    return render(request, "contact_form/contact.html", {'form': form})
