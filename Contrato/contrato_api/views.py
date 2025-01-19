from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Contrato, Parcela
from .serializers import ContratoSerializer, ParcelaSerializer

class ContratoListApiView(APIView):
    # add permission to check if user is authenticated
    classe_permissao = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
      #  contratos = Contrato.objects.filter(id_contrato = request.data.get('id_contrato'))
        contratos = Contrato.objects
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
