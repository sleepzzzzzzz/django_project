from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [

    path('', views.HomeTemplateView.as_view(), name='home'),
    path('men/', views.MenTemplate.as_view(), name='Men'),
    path('women/', views.women, name='Women'),
    path('kids/', views.kids, name='Kids'),
    path('accessories/', views.accessory, name='Accessory'),

    path('category/<slug:category_slug>/', views.one_cat, name='one_cat'),
    path('product/<slug:product_slug>/', views.prod_view, name='prod_view'),
    path('addon/<slug:addon_slug>/', views.addon_view, name='addon_view'),

    # path('ad/', views.addons, name='addons'),
    # path('addon/<slug:addon_slug>/', views.addon_view, name='addon_view'),
    # path('onec/', views.one_cat, name='one_cat'),
    # path('onec/<slug:product_slug>/', views.product_views, name='product'),

    # path('product/', views.product_views, name='product'),
    # path('category/<slug:category_slug>/', views.category_view, name='category_view'),
    # path('product/<slug:product_slug>/', views.prod_view, name='prod_view'),
    # path('category/<slug:category_slug>/', views.cat_review, name='cat_review'),
    # path('product/<slug:product_slug>/', views.prod_review, name='prod_review'),
    # path('cat/<slug:category_slug>/', views.table, name='table'),

]
