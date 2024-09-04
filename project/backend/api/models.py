# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class UpdateDate(models.Model):
    last_update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.last_update)

class Cpvlicitacion(models.Model):
    id_combinacion = models.AutoField(primary_key=True)
    id_licitacion = models.ForeignKey('Licitaciones', models.DO_NOTHING, db_column='id_licitacion')
    id_cpv = models.ForeignKey('Codigoscpv', models.DO_NOTHING, db_column='id_cpv')

    class Meta:
        managed = False
        db_table = 'CPVLicitacion'


class Codigoscpv(models.Model):
    id_cpv = models.AutoField(primary_key=True)
    num_cpv = models.CharField(max_length=500, db_collation='Modern_Spanish_CI_AS')
    descripcion = models.CharField(max_length=500, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CodigosCPV'


class Criterios(models.Model):
    id_criterio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200, db_collation='Modern_Spanish_CI_AS')
    siglas = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    valor_max = models.FloatField(blank=True, null=True)
    valor_min = models.FloatField(blank=True, null=True)
    id_padre = models.ForeignKey('self', models.DO_NOTHING, db_column='id_padre', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Criterios'


class Empresas(models.Model):
    id_empresa = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=200, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    nif = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    pyme = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Empresas'



class Licitaciones(models.Model):
    id_licitacion = models.AutoField(primary_key=True) 
    num_expediente = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS') #basic
    abonos_cuenta = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True) #importe
    clasificacion_subgrupo = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    clasificacion_grupo = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    clasificacion_cat = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    importe_con_impuestos = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    importe_sin_impuestos = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    criterios_economica = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    criterios_tecnica = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    criterios_valores_anormales = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    condiciones_especiales = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    infraccion_grave = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    contratacion_control = models.BooleanField(blank=True, null=True)
    crit_adjudicacion = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    fecha_adjudicacion = models.DateField(blank=True, null=True)
    fecha_formalizacion = models.DateField(blank=True, null=True)
    fecha_anuncio = models.DateField(blank=True, null=True)
    forma_pago = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    garantia_def = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    garantia_prov = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    gastos_desistimiento = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    modificaciones_prev = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    prorrogas_prev = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    revision_precios_prev = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    otros_conceptos_prev = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    inclusion_control_calidad = models.BooleanField(blank=True, null=True)
    lugar_ejecucion = models.CharField(max_length=1000, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    medios_economica = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    medios_tecnica = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    mejora_criterio = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    objeto = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    obligacion_subcontratacion = models.BooleanField(blank=True, null=True)
    otros_componentes = models.CharField(max_length=200, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    penalidades_incumplimiento = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    plazo_ejecucion = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    plazo_garantia = models.CharField(max_length=2000, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    plazo_presentacion = models.DateField(blank=True, null=True)
    plazo_recepcion = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    plazo_maximo_prorrogas = models.CharField(max_length=200, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    ampliacion_presentacion = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    porcentaje_max_subcontratacion = models.FloatField(blank=True, null=True)
    posibilidad_prorroga = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    procedimiento = models.ForeignKey('Tipoprocedimiento', models.DO_NOTHING, db_column='procedimiento', blank=True, null=True)
    pag_info_criterios = models.IntegerField(blank=True, null=True)
    regimen_penalidades = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    revision_precios = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    sistema_precios = models.CharField(max_length=1000, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    subasta_electronica = models.BooleanField(blank=True, null=True)
    subcontratacion_criterio = models.BooleanField(blank=True, null=True)
    tareas_criticas = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    tipo_contrato = models.ForeignKey('Tipocontrato', models.DO_NOTHING, db_column='tipo_contrato', blank=True, null=True)
    tramitacion = models.ForeignKey('Tipotramitacion', models.DO_NOTHING, db_column='tramitacion', blank=True, null=True)
    unidad_encargada = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    valor_estimado = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    adjudicatario = models.ForeignKey(Empresas, models.DO_NOTHING, db_column='adjudicatario', blank=True, null=True)
    num_incursas_anormalidad = models.IntegerField(blank=True, null=True)
    num_invitadas = models.IntegerField(blank=True, null=True)
    num_seleccionadas = models.IntegerField(blank=True, null=True)
    num_licitadores = models.IntegerField(blank=True, null=True)
    num_excluidas = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Licitaciones'


class Links(models.Model):
    id_link = models.AutoField(primary_key=True)
    link = models.CharField(max_length=200, db_collation='Modern_Spanish_CI_AS')
    type_link = models.ForeignKey('Tipolink', models.DO_NOTHING, db_column='type_link')
    id_licitacion = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Links'


class Participaciones(models.Model):
    id_participacion = models.AutoField(primary_key=True)
    id_licitacion = models.ForeignKey(Licitaciones, models.DO_NOTHING, db_column='id_licitacion')
    id_empresa = models.ForeignKey(Empresas, models.DO_NOTHING, db_column='id_empresa')
    importe_ofertado_sin_iva = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    importe_ofertado_con_iva = models.DecimalField(max_digits=19, decimal_places=4, blank=True, null=True)
    excluida = models.BooleanField(blank=True, null=True)
    anormalidad_economica = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Participaciones'


class Tipocontrato(models.Model):
    id_tipo_contrato = models.AutoField(primary_key=True)
    nombre_tipo_contrato = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS')

    class Meta:
        managed = False
        db_table = 'TipoContrato'


class Tipolink(models.Model):
    id_tipo_link = models.AutoField(primary_key=True)
    texto_tipo_link = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS')

    class Meta:
        managed = False
        db_table = 'TipoLink'


class Tipoprocedimiento(models.Model):
    id_procedimiento = models.AutoField(primary_key=True)
    nombre_procedimiento = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS')

    class Meta:
        managed = False
        db_table = 'TipoProcedimiento'


class Tipotramitacion(models.Model):
    id_tramitacion = models.AutoField(primary_key=True)
    nombre_tramitacion = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS')

    class Meta:
        managed = False
        db_table = 'TipoTramitacion'


class Valoraciones(models.Model):
    id_valoracion = models.AutoField(primary_key=True)
    id_participacion = models.ForeignKey(Participaciones, models.DO_NOTHING, db_column='id_participacion')
    id_criterio = models.ForeignKey(Criterios, models.DO_NOTHING, db_column='id_criterio')
    puntuacion = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Valoraciones'


class ApiItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS')
    description = models.TextField(db_collation='Modern_Spanish_CI_AS')

    class Meta:
        managed = False
        db_table = 'api_item'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, db_collation='Modern_Spanish_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, db_collation='Modern_Spanish_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, db_collation='Modern_Spanish_CI_AS')
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, db_collation='Modern_Spanish_CI_AS')
    first_name = models.CharField(max_length=150, db_collation='Modern_Spanish_CI_AS')
    last_name = models.CharField(max_length=150, db_collation='Modern_Spanish_CI_AS')
    email = models.CharField(max_length=254, db_collation='Modern_Spanish_CI_AS')
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    object_repr = models.CharField(max_length=200, db_collation='Modern_Spanish_CI_AS')
    action_flag = models.SmallIntegerField()
    change_message = models.TextField(db_collation='Modern_Spanish_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS')
    model = models.CharField(max_length=100, db_collation='Modern_Spanish_CI_AS')

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, db_collation='Modern_Spanish_CI_AS')
    name = models.CharField(max_length=255, db_collation='Modern_Spanish_CI_AS')
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40, db_collation='Modern_Spanish_CI_AS')
    session_data = models.TextField(db_collation='Modern_Spanish_CI_AS')
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128, db_collation='Modern_Spanish_CI_AS')
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)
