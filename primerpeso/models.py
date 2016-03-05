from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import ugettext as _
from localflavor.us.models import USStateField, USZipCodeField


class WhoAndWhenBase(models.Model):
    """An abstract base class which manages created at and updated at as well as
    who created it.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated_at'))
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('creator'))

    class Meta:
        abstract = True


class Agency(WhoAndWhenBase):
    """A government or NGO organization which manages ``Opportunities``.
    """
    id = models.IntegerField(primary_key=True, verbose_name=_('id'))
    name = models.CharField(max_length=255, unique=True, verbose_name=_('name'))
    mission = models.TextField(blank=True, verbose_name=_('mission'))
    phone = models.CharField(blank=True, max_length=255, verbose_name=_('phone'))
    fax = models.CharField(blank=True, max_length=255, verbose_name=_('fax'))
    email = models.EmailField(blank=True, verbose_name=_('email'))
    address = models.TextField(blank=True, verbose_name=_('address'))
    municipality = models.CharField(blank=True, max_length=255, verbose_name=_('municipality'))
    state = USStateField(blank=True)
    postal_code = USZipCodeField(blank=True)  # zip is a global function
    web = models.URLField(max_length=255, blank=True, verbose_name=_('web'))

    class Meta:
        verbose_name = _('Agency')
        verbose_name_plural = _('Agencies')


class Requirement(WhoAndWhenBase):
    """An ``Opportunity`` can have multiple ``Requirements`` each represent
    a different step to utilitizing it.
    """
    id = models.IntegerField(primary_key=True, verbose_name=_('id'))
    name = models.CharField(max_length=255, unique=True, verbose_name=_('name'))
    description = models.TextField(blank=True, verbose_name=_('description'))
    provider = models.CharField(blank=True, max_length=255, verbose_name=_('provider'))
    link = models.TextField(blank=True, verbose_name=_('link'))
    cost = models.TextField(blank=True, verbose_name=_('cost'))

    class Meta:
        verbose_name = _('Requirement')
        verbose_name_plural = _('Requirements')


class RequirementRelationship(WhoAndWhenBase):
    opportunity = models.ForeignKey('Opportunity', verbose_name=_('opportunity'))
    requirement = models.ForeignKey(Requirement, verbose_name=_('requirement'))

    class Meta:
        verbose_name = _('Requirement Relationship')
        verbose_name_plural = _('Requirement Relationships')


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

BENEFIT_TYPES = (('incentive', 'Incentivos'),
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
    id = models.IntegerField(primary_key=True, verbose_name=_('id'))
    title = models.CharField(max_length=255, unique=True, verbose_name=_('title'))
    gender = models.CharField(max_length=6,
                              choices=(('male', _('Male')),
                                       ('female', _('Female')),
                                       ('any', _('Any')),
                                       ('other', _('Other')),))
    application_cost = models.IntegerField(verbose_name=_('application cost'))
    application_deadline = models.DateTimeField(null=True, blank=True, verbose_name=_('application deadline'))
    benefit_description = models.TextField(verbose_name=_('benefit description'))
    agency_contact_name = models.CharField(max_length=255, verbose_name=_('agency contact name'))
    agency_contact_phone = models.CharField(max_length=255, verbose_name=_('agency contact phone'))
    agency_contact_email = models.EmailField(verbose_name=_('agency contact email'))
    minimum_years_in_business = models.IntegerField(verbose_name=_('minimum years in business'))
    additional_information = models.TextField(verbose_name=_('additional information'))
    investing_own_money = models.BooleanField(verbose_name=_('investing own money'))
    money_invested = models.CharField(max_length=255, verbose_name=_('money invested'))
    agency = models.ForeignKey(Agency, verbose_name=_('agency'))
    requirement = models.ManyToManyField(Requirement, through=RequirementRelationship, verbose_name=_('requirement'))
    age_min = models.IntegerField(verbose_name=_('minimum age'))
    age_max = models.IntegerField(null=True, blank=True, verbose_name=_('maximum age'))
    employees_min = models.IntegerField(verbose_name=_('minimum employees'))
    employees_max = models.IntegerField(null=True, blank=True, verbose_name=_('maximum employees'))
    annual_revenue_min = models.IntegerField(verbose_name=_('minimum annual revenue'))
    annual_revenue_max = models.IntegerField(null=True, blank=True, verbose_name=_('maximum annual revenue'))
    average_application_time = models.CharField(max_length=255, blank=True, verbose_name=_('average application time'))
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


class OpportunitySearch(models.Model):
    """A government sponsored incentive/grant/tax break for businessses local
    to Puerto Rico.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    email = models.EmailField(verbose_name=_('What is your email?'))
    purpose = ArrayField(
        models.CharField(max_length=255, choices=PURPOSE),
        default=list, verbose_name=_('How would you use the incentive?'),
    )
    investing_own_money = models.BooleanField(verbose_name=_('Will you invest personal money?'))

    gender = models.CharField(max_length=6,
                              choices=(('male', _('Male')),
                                       ('female', _('Female')),
                                       ('both', _('Both')),
                                       ('other', _('Other')),),
                              verbose_name=_("What are the owner's genders?"),
                              )
    age = models.IntegerField(verbose_name=_('What is the age of the owners?'))

    entity_type = models.CharField(max_length=255, choices=ENTITY_TYPES, verbose_name=_('What is the business structure?'))
    industry = models.CharField(max_length=255, choices=INDUSTRIES, verbose_name=_('What industry is your business?'))

    locations = ArrayField(
        models.CharField(max_length=255, choices=LOCATIONS),
        default=list,
        verbose_name=_('Where is your business located?'),
    )

    employees = models.IntegerField(verbose_name=_('How many full time employees do you have?'))
    years_in_business = models.IntegerField(verbose_name=_('How many years have you been in business?'))
    annual_revenue = models.IntegerField(verbose_name=_('What is your annual revenue?'))

    def search(self):
        opps = Opportunity.objects
        for purpose in self.purpose:
            opps = opps.filter(purpose__contains=[purpose,])
        if self.investing_own_money:
            opps = opps.filter(investing_own_money=True)
        genders = ['any']
        if self.gender == 'both':
            genders.extend(['male', 'female'])
        else:
            genders.append(self.gender)
        opps = opps.filter(gender__in=genders)
        opps = opps.filter(age_min__lte=self.age).filter(age_max__gte=self.age)
        if self.entity_type != 'any':
            opps = opps.filter(entity_types__contains=[self.entity_type,])
        if self.industry != 'any':
            opps = opps.filter(industries__contains=[self.industry,])
        for location in self.locations:
            opps = opps.filter(locations__contains=[location,])
        opps = opps.filter(employees_min__lte=self.employees).\
                    filter(employees_max__gte=self.employees)
        return opps


    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('Opportunity Search')
        verbose_name_plural = _('Opportunity Searches')
