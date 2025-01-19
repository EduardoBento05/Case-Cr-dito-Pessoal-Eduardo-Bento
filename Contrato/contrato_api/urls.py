from django.urls import path, include
from .views import (
    ContratoListApiView,
)

urlpatterns = [
    path('api', ContratoListApiView.as_view()),
]
