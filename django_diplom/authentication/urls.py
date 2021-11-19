from django.urls import path

from . import views

app_name = 'authentication'

urlpatterns = [
    path('reg/', views.reg, name='reg'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('myacc/', views.account, name='account'),


]
