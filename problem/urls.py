from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.lister, name='problem_list'),
    path('list', views.lister, name='problem_list'),
    path('detail/', views.detail, name='problem_detail'),
    path('detail', views.detail, name='problem_detail'),
    path('submit/', views.submit, name='problem_submit'),
    path('submit', views.submit, name='problem_submit'),
]
