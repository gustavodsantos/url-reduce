from django.urls import path

from mysite.encurtador import views

app_name = 'encurtador'

urlpatterns = [
    path('', views.home, name='home'),
    path('criar_url/', views.criar_url, name='criar_url'),
    path('<slug:slug>/', views.redirecionar, name='redirecionar'),
    path('relatorios/<slug:slug>', views.relatorios, name='relatorios'),
]
