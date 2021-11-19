from django.urls import path
from . import views

app_name = 'new'

urlpatterns = [

    path('news/', views.new, name='new'),
]


