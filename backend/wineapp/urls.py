from django.urls import path
from . import views
urlpatterns = [
    path('health/', views.health),
    path('analysis/', views.analysis),
    path('dataset/', views.dataset),
    path('export/', views.export),
    path('predict/', views.predict),
    path('predictions/', views.predictions),
]
