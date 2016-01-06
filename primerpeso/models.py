from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext as _
from localflavor.us.models import USStateField, USPostalCodeField


class WhoAndWhenBase(models.Model):
    """An abstract base class which manages created at and updated at as well as
    who created it.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True


class Agency(WhoAndWhenBase):
    """A government or NGO organization which manages ``Opportunities``.
    """
    name = models.CharField(max_length=255, unique=True)
    mission = models.TextField(blank=True)
    phone = models.CharField(blank=True, max_length=255)
    fax = models.CharField(blank=True, max_length=255)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    municipality = models.CharField(blank=True, max_length=255)
    state = USStateField(blank=True)
    postal_code = USPostalCodeField(blank=True)  # zip is a global function
    web = models.URLField(max_length=255, blank=True)


class Requirement(WhoAndWhenBase):
    """An ``Opportunity`` can have multiple ``Requirements`` each represent
    a different step to utilitizing it.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    provider = models.CharField(blank=True, max_length=255)
    link = models.TextField(blank=True)
    cost = models.TextField(blank=True)

LOCATIONS = (('anywhere_in_pr', 'Cualquier municipio'),
             ('adjuntas', 'Adjuntas'),
             ('aguada', 'Aguada'),
             ('aguadilla', 'Aguadilla'),
             ('aguas_buenas', 'Aguas Buenas'),
             ('aibonito', 'Aibonito'),
             ('anasco', 'Añasco'),
             ('arecibo', 'Arecibo'),
             ('arroyo', 'Arroyo'),
             ('barceloneta', 'Barceloneta'),
             ('barranquitas', 'Barranquitas'),
             ('bayamon', 'Bayamón'),
             ('cabo_rojo', 'Cabo Rojo'),
             ('caguas', 'Caguas'),
             ('camuy', 'Camuy'),
             ('canovanas', 'Canóvanas'),
             ('carolina', 'Carolina'),
             ('catano', 'Cataño'),
             ('cayey', 'Cayey'),
             ('ceiba', 'Ceiba'),
             ('ciales', 'Ciales'),
             ('cidra', 'Cidra'),
             ('coamo', 'Coamo'),
             ('comerio', 'Comerio'),
             ('corozal', 'Corozal'),
             ('culebra', 'Culebra'),
             ('dorado', 'Dorado'),
             ('fajardo', 'Fajardo'),
             ('florida', 'Florida'),
             ('guanica', 'Guánica'),
             ('guayama', 'Guayama'),
             ('guayanilla', 'Guayanilla'),
             ('guaynabo', 'Guaynabo'),
             ('gurabo', 'Gurabo'),
             ('hatillo', 'Hatillo'),
             ('hormigueros', 'Hormigueros'),
             ('humacao', 'Humacao'),
             ('isabela', 'Isabela'),
             ('jayuya', 'Jayuya'),
             ('juana_diaz', 'Juana Diaz'),
             ('juncos', 'Juncos'),
             ('lajas', 'Lajas'),
             ('lares', 'Lares'),
             ('las_marias', 'Las Marías'),
             ('las_piedras', 'Las Piedras'),
             ('loiza', 'Loíza'),
             ('luquillo', 'Luquillo'),
             ('manati', 'Manatí'),
             ('maricao', 'Maricao'),
             ('maunabo', 'Maunabo'),
             ('mayaguez', 'Mayagüez'),
             ('moca', 'Moca'),
             ('morovis', 'Morovis'),
             ('naguabo', 'Naguabo'),
             ('naranjito', 'Naranjito'),
             ('orocovis', 'Orocovis'),
             ('patillas', 'Patillas'),
             ('penuelas', 'Penuelas'),
             ('ponce', 'Ponce'),
             ('quebradillas', 'Quebradillas'),
             ('rincon', 'Rincón'),
             ('rio_grande', 'Río Grande'),
             ('sabana_grande', 'Sabana Grande'),
             ('salinas', 'Salinas'),
             ('san_german', 'San German'),
             ('san_juan', 'San Juan'),
             ('san_lorenzo', 'San Lorenzo'),
             ('san_sebastian', 'San Sebastian'),
             ('santa_isabel', 'Santa Isabel'),
             ('toa_alta', 'Toa Alta'),
             ('toa_baja', 'Toa Baja'),
             ('trujillo_alto', 'Trujillo Alto'),
             ('utuado', 'Utuado'),
             ('vega_alta', 'Vega Alta'),
             ('vega_baja', 'Vega Baja'),
             ('vieques', 'Vieques'),
             ('villalba', 'Villalba'),
             ('yabucoa', 'Yabucoa'),
             ('yauco', 'Yauco'))

ENTITY_TYPES = (('any', 'Cualquier'),
                ('non_profit', 'Organización sin fines de lucro'),
                ('for_profit', 'Corporación o Asociación con fines de lucro '),
                ('sole_proprietor', 'Individuo (DBA-HNC)'),
                ('cooperative', 'Cooperativa'),)

INDUSTRIES = (('any', 'Cualquiera'),
              ('11', '11 - Agricultura, Silvicultura, Caza y Pesca'),
              ('21', '21 - Extracción de Gas y Petróleo'),
              ('22', '22 - Utilidades'),
              ('23', '23 - Construcción'),
              ('31-33', '31-33 Manufactura'),
              ('42', '42 - Comercio al por mayor'),
              ('44-45', '44-45 - Comercio al por menor'),
              ('48-49', '48-49 - Transporte y Almacén'),
              ('51', '51 - Información'),
              ('52', '52 - Finanzas y Seguros'),
              ('53', '53 - Bienes Raíces, Alquiler y Arrendamiento'),
              ('54', '54 - Servicios profesionales, científicos y técnicos'),
              ('56', '56 - Administración y apoyo, central de desechos y servicios de reparación'),
              ('61', '61 - Servicios educativos'),
              ('62', '62 - Cuidados de salud y asistencia social'),
              ('71', '71 - Artes, Entretenimiento y Recreación'),
              ('72', '72 - Alojamiento, Servicios de Alimentos y Lugares para Beber'),
              ('81', '81 - Otros Servicios (exceptuando la administración pública)'),
              ('92', '92 - Administración Pública'),
              ('other', 'Otra'),)

DEMOGRAPHICS = (('any', 'cualquiera'),
                ('student', 'estudiante'),
                ('veteran', 'veterano'),
                ('minority', 'minoría'),)

BENEFIT_TYPES =  (('incentive', 'Incentivos'),
                  ('loan', 'Créditos'),
                  ('grant', 'Becas'),
                  ('reimbursement', 'Reembolsos'),
                  ('expertise', 'Talleres'),
                  ('financing', 'Financiamiento'),
                  ('other', 'Otros'),)

PURPOSE = (('anything', 'Cualquiera'),
           ('open_location', 'Abrir un Nuevo Local'),
           ('open_franchise', 'Abrir una Franquicia'),
           ('train_employees', 'Adiestrar Empleados'),
           ('working_capital', 'Capital de trabajo'),
           ('buy_equipment', 'Comprar Equipo'),
           ('buy_commercial_property', 'Comprar una propiedad comercial'),
           ('hire_employees', 'Contratar Empleados  / Pasantes'),
           ('start_business', 'Crear un Negocio'),
           ('export', 'Exportar'),
           ('export_products', 'Exportar productos'),
           ('export_services', 'Exportar servicios'),
           ('improve_commercial_property', 'Mejorar una propiedad comercial'),
           ('cinematographic_production', 'Producción Cinematográfica'),
           ('keep_employees', 'Retener empleados'),
           ('relocate_business', 'Reubicar un Negocio'),
           ('other', 'Otro (Por favor especifíca el propósito)'),)


class Opportunity(WhoAndWhenBase):
    """A government sponsored incentive/grant/tax break for businessses local
    to Puerto Rico.
    """
    title = models.CharField(max_length=255, unique=True)
    gender = models.CharField(max_length=6,
                              choices=(('male', _('Male')),
                                       ('female', _('Female')),
                                       ('any', _('Any')),
                                       ('other', _('Other')),))
    application_cost = models.IntegerField()
    application_deadline = models.DateField()
    benefit_description = models.TextField()
    agency_contact_name = models.CharField(max_length=255)
    agency_contact_phone = models.CharField(max_length=255)
    agency_contact_email = models.EmailField()
    minimum_years_in_business = models.IntegerField()
    additional_information = models.TextField()
    investing_own_money = models.BooleanField()
    money_invested = models.CharField(max_length=255)
    agency = models.ForeignKey(Agency)
    requirement = models.ManyToMany(Requirement)
    age_min = models.IntegerField()
    age_max = models.IntegerField(null=True, blank=True)
    employees_min = models.IntegerField()
    employees_max = models.IntegerField(null=True, blank=True)
    annual_revenue_min = models.IntegerField()
    annual_revenue_max = models.IntegerField(null=True, blank=True)
    average_application_time = models.CharField(max_length=255, blank=True)
    locations = ArrayField(
        models.CharField(max_length=255, choices=LOCATIONS),
        default=list,
    )
    entity_types = ArrayField(
        models.CharField(max_length=255, choices=ENTITY_TYPES),
        default=list,
    )
    industries = ArrayField(
        models.CharField(max_length=255, choices=INDUSTRIES),
        default=list,
    )
    demographics = ArrayField(
        models.CharField(max_length=255, choices=DEMOGRAPHICS),
        default=list,
        blank=True,
    )
    benefit_types = ArrayField(
        models.CharField(max_length=255, choices=BENEFIT_TYPES),
        default=list,
    )
    purpose = ArrayField(
        models.CharField(max_length=255, choices=PURPOSE),
        default=list,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Opportunity')
        verbose_name_plural = _('Opportunities')
