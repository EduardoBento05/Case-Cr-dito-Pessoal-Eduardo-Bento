from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Contrato, Parcela
from .serializers import ContratoSerializer, ParcelaSerializer
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Avg



class ContratoListApiView(APIView):
    # add permission to check if user is authenticated
    classe_permissao = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
      #  contratos = Contrato.objects.filter(id_contrato = request.data.get('id_contrato'))
        contratos = Contrato.objects.all()
        cpf_tomador = request.query_params.get('cpf_tomador')
        data_emissao = request.query_params.get('data_emissao')
        endereco_estado = request.query_params.get('endereco_estado')

        if cpf_tomador:
            contratos = contratos.filter(cpf_tomador = cpf_tomador)
        elif data_emissao:
            contratos = contratos.filter(data_emissao = data_emissao)
        elif endereco_estado:
            contratos = contratos.filter(endereco_estado = endereco_estado)

        serializer = ContratoSerializer(contratos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {

            'data_emissao': request.data.get('dataEmissao'),
            'data_nascimento_tomador': request.data.get('dataNascimentoTomador'),
            'valor_desembolsado': request.data.get('valorDesembolsado'),
            'cpf_tomador': request.data.get('cpfTomador'),
            'endereco_pais': request.data.get('enderecoPais'),
            'endereco_estado': request.data.get('enderecoEstado'),
            'endereco_cidade': request.data.get('enderecoCidade'),
            'telefone_tomador': request.data.get('telefoneTomador'),
            'taxa_contrato': request.data.get('taxaContrato'),
        }
        serializer = ContratoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContratoViewSet(ModelViewSet):
    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id_contrato', 'cpf_tomador', 'data_emissao', 'endereco_estado']


    @action(detail=False, methods=['get'])
    def resumo(self, request):
        contratos = self.filter_queryset(self.get_queryset())

        valor_total_receber = contratos.aggregate(total=Sum('parcelas__valor_parcela'))['total'] or 0

        valor_total_desembolsado = contratos.aggregate(total=Sum('valor_desembolsado'))['total'] or 0

        numero_total_contratos = contratos.count()

        taxa_media = contratos.aggregate(media=Avg('taxa_contrato'))['media'] or 0

        return Response({
            "valor_total_receber": valor_total_receber,
            "valor_total_desembolsado": valor_total_desembolsado,
            "numero_total_contratos": numero_total_contratos,
            "taxa_media": taxa_media
        })
