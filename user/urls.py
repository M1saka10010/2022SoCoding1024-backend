from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('register/', views.register, name='register'),
    path('info', views.info, name='info'),
    path('info/', views.info, name='info'),
    path('update', views.update, name='update'),
    path('update/', views.update, name='update'),
]
