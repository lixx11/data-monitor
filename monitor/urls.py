from django.urls import path, re_path

from . import views


urlpatterns = [
    path('', views.index),
    path('data_summary/', views.data_summary),
    path('data/<str:filename>', views.data)
]
