from django.db import models

class Contrato(models.Model):
    id_contrato = models.AutoField(primary_key=True)
    data_emissao = models.DateField(auto_now_add=True)
    data_nascimento_tomador = models.DateField()
    valor_desembolsado = models.DecimalField(max_digits=10, decimal_places=2)
    cpf_tomador = models.CharField(max_length=11, unique=True)
    endereco_pais = models.CharField(max_length=50)
    endereco_estado = models.CharField(max_length=50)
    endereco_cidade = models.CharField(max_length=50)
    telefone_tomador = models.CharField(max_length=15)
    taxa_contrato = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return  self.id_contrato


class Parcela(models.Model):
    contrato = models.ForeignKey(Contrato, related_name='parcelas', on_delete=models.CASCADE)
    numero_parcela = models.IntegerField()
    valor_parcela = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()

    def __str__(self):
        return self.numero_parcela
