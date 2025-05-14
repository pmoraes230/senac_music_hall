from django.db import models

class Perfil(models.Model):
    nome = models.CharField(max_length=45, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'perfil'

    def __str__(self):
        return self.nome
    
class Usuario(models.Model):
    nome = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    id_perfil = models.ForeignKey(Perfil, models.DO_NOTHING, db_column='id_perfil')
    login = models.CharField(max_length=25, blank=True, null=True)
    senha = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'

    def __str__(self):
        return self.nome

class Setores(models.Model):
    nome = models.CharField(max_length=45, blank=True, null=True)
    qtd_cadeira = models.IntegerField()
    valor_setor = models.FloatField()
    status = models.CharField(max_length=9)

    class Meta:
        managed = False
        db_table = 'setores'

    def __str__(self):
        return self.nome

class Evento(models.Model):
    nome = models.CharField(max_length=45)
    data_evento = models.DateField()
    capacidade_pessoas = models.IntegerField()
    id_setores = models.ForeignKey(Setores, models.DO_NOTHING, db_column='id_setores')

    class Meta:
        managed = False
        db_table = 'evento'

    def __str__(self):
        return self.nome

class Venda(models.Model):
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario')
    id_evento = models.ForeignKey(Evento, models.DO_NOTHING, db_column='id_evento')
    valor_final = models.FloatField()
    data_venda = models.DateField()

    class Meta:
        managed = False
        db_table = 'venda'

    def __str__(self):
        return str(f'Ingresso vendido a {self.id_usuario}, no evento: {self.id_evento}')
