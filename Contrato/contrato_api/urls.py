from django.urls import path
from .views import ContratoListApiView, ContratoViewSet


contrato_list = ContratoViewSet.as_view({'get': 'list'})
resumo_view = ContratoViewSet.as_view({'get': 'resumo'})

urlpatterns = [
    path('api/', ContratoListApiView.as_view(), name='contrato-list-api'),
    path('api/contratos/', contrato_list, name='contrato-list'),
    path('api/contratos/resumo/', resumo_view, name='contrato-resumo'),
]