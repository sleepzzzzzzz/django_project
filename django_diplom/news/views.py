from django.shortcuts import render

# Create your views here.
from news.models import New


def new(request, new_slug):
    new = New.objects.prefetch_related("news_set").filter(slug=new_slug).first()

    return render(
        request,
        'news/news.html',
        {"news": new}
    )