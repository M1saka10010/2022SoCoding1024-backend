from django.urls import path

from . import views

urlpatterns = [
    path('my/', views.my_rank, name='my_rank'),
    path('my', views.my_rank, name='my_rank'),
    path('list/', views.ranking, name='problem_list'),
    path('list', views.ranking, name='problem_list'),
]
