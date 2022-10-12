import os
import django_filters

from django import forms
from django_currentuser.db.models import CurrentUserField
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import Profile
from reference_books.models import Client, Branches, ModelEquipment, UrgencyRepairs, Section, MonthList, Parts, \
    StatusWork, StageProduction, ResultsDetailTechProcess, StatusAvailability, Material, StatusReceiving, StatusTask, \
    TreeTechProcessStage
from tasks.models import Tasks


def validate_file_photo(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Файл не поддерживается.')


def photo_file_rename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "shipment_id%s.%s" % (str(instance.id), ext)
    return os.path.join('shipment/', filename)


class Shipment(models.Model):
    branch = models.ForeignKey(Branches, verbose_name=u'Филиал', on_delete=models.CASCADE)
    specificationnum = models.CharField(u'Номер спецификации', max_length=10)
    client = models.ForeignKey(Client, models.SET_NULL, verbose_name=u'Контрагент', null=True)
    dateshipment = models.DateField(u'Дата поставки')
    photo = models.ImageField(u'Фотография поставки')   #, width_field=1000, height_field=800, upload_to=photo_file_rename)

    create_user = CurrentUserField(related_name='sh_creator', on_update=False)
    update_user = CurrentUserField(related_name='sh_modifying', on_update=True)

    datetime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    datetime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    def __str__(self):
        return 'Спецификация №' + str(self.specificationnum)

    class Meta:
        verbose_name = u'Поставка'
        verbose_name_plural = u'Список поставок на ремонт '


class ScopeShipment(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    repairnum = models.CharField(u'Ремонтный номер', max_length=10)
    equipment = models.ForeignKey(ModelEquipment, verbose_name=u'Модель оборудования', blank=True, null=True,
                                  on_delete=models.CASCADE)
    urgency = models.ForeignKey(UrgencyRepairs, verbose_name=u'Срочность ремонта',
                                on_delete=models.CASCADE)
    shedulemonth = models.ForeignKey(MonthList, verbose_name=u'Месяц', blank=True, null=True,
                                     on_delete=models.CASCADE)
    stage = models.ForeignKey(StageProduction, verbose_name=u'Стадии производства', blank=True, null=True,
                              on_delete=models.CASCADE)
    section = models.CharField(u'Участок', choices=Section, max_length=10)
    estimate = models.BooleanField(u'Смета', default=False)
    status = models.ForeignKey(StatusWork, verbose_name=u'Общий статус ремонта', on_delete=models.CASCADE)
    order = models.BooleanField(u'Заказ на производство', default=False)
    executor = models.ForeignKey(Profile, verbose_name=u'Ответственный исполнитель', blank=True, null=True,
                                 on_delete=models.CASCADE)

    dateready = models.DateField(u'Дата готовности', blank=True, null=True)

    archive = models.BooleanField(u'Архив', default=False)

    stage_poles = models.ForeignKey(TreeTechProcessStage, verbose_name=u'Стадия', blank=True, null=True,
                                    related_name='stage_poles', on_delete=models.CASCADE)
    stage_sections = models.ForeignKey(TreeTechProcessStage, verbose_name=u'Стадия', blank=True, null=True,
                                       related_name='stage_sections', on_delete=models.CASCADE)
    stage_inductor = models.ForeignKey(TreeTechProcessStage, verbose_name=u'Стадия', blank=True, null=True,
                                       related_name='stage_inductor', on_delete=models.CASCADE)
    stage_anchor = models.ForeignKey(TreeTechProcessStage, verbose_name=u'Стадия', blank=True, null=True,
                                     related_name='stage_anchor', on_delete=models.CASCADE)
    stage_shields = models.ForeignKey(TreeTechProcessStage, verbose_name=u'Стадия', blank=True, null=True,
                                      related_name='stage_shields', on_delete=models.CASCADE)
    stage_spindle = models.ForeignKey(TreeTechProcessStage, verbose_name=u'Стадия', blank=True, null=True,
                                      related_name='stage_spindle', on_delete=models.CASCADE)

    disassembly_time = models.DateField(u'Срок разборки', blank=True, null=True)
    faultdetection_time = models.DateField(u'Срок дефектовки', blank=True, null=True)
    storage_time = models.DateField(u'Срок склад', blank=True, null=True)
    poles_time = models.DateField(u'Срок полюса', blank=True, null=True)
    sections_time = models.DateField(u'Срок секции', blank=True, null=True)
    inductor_time = models.DateField(u'Срок индуктор', blank=True, null=True)
    anchor_time = models.DateField(u'Срок якорь', blank=True, null=True)
    shields_time = models.DateField(u'Срок щиты', blank=True, null=True)
    spindle_time = models.DateField(u'Срок вал', blank=True, null=True)
    completing_time = models.DateField(u'Срок комплектования', blank=True, null=True)
    assembly_time = models.DateField(u'Срок сборки', blank=True, null=True)
    conservation_time = models.DateField(u'Срок консервации', blank=True, null=True)

    complete_disassembly = models.BooleanField(u'Разбор - принято', default=False)
    complete_faultdetection = models.BooleanField(u'Дефектация - принято', default=False)
    complete_mechanics = models.BooleanField(u'Механика - принято', default=False)
    complete_tests = models.BooleanField(u'Тестирование - принято', default=False)
    complete_poles = models.BooleanField(u'Полюса - принято', default=False)
    complete_sections = models.BooleanField(u'Секции - принято', default=False)
    complete_inductor = models.BooleanField(u'Индуктор - принято', default=False)
    complete_anchor = models.BooleanField(u'Якорь - принято', default=False)
    complete_shields = models.BooleanField(u'Щиты - принято', default=False)
    complete_spindle = models.BooleanField(u'Вал - принято', default=False)
    complete_completing = models.BooleanField(u'Комплектующие - принято', default=False)
    complete_assembly = models.BooleanField(u'Сборка - принято', default=False)

    create_user = CurrentUserField(related_name='sc_create_user', on_update=False)
    update_user = CurrentUserField(related_name='sc_update_user', on_update=True)

    datetime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    datetime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    def __str__(self):
        return 'Ремонтный №' + str(self.repairnum)

    class Meta:
        verbose_name = u'Оборудование'
        verbose_name_plural = u'Состав поставки '


class ScopeShipmentEngineFilter(django_filters.FilterSet):
    client = django_filters.ModelChoiceFilter(label=u'Контрагент', queryset=Client.objects.all(),
                                              field_name="shipment__client")
    specnum = django_filters.CharFilter(label=u'Номер спецификации', field_name="shipment__specificationnum",
                                        lookup_expr='icontains')
    eq = django_filters.ModelChoiceFilter(label=u'Модель', queryset=ModelEquipment.objects.all(),
                                          field_name="equipment")
    eq_p = django_filters.NumberFilter(label=u'P', field_name="equipment__p", lookup_expr='')
    eq_u = django_filters.NumberFilter(label=u'u', field_name="equipment__u")
    eq_n = django_filters.NumberFilter(label=u'n', field_name="equipment__n")
    winding_time = django_filters.DateFilter(label=u'Срок обмотки', input_formats=('%Y-%m-%d',),
                                             widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))
    assembly_time = django_filters.DateFilter(label=u'Срок сборки', input_formats=('%Y-%m-%d',),
                                              widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}))

    class Meta:
        model = ScopeShipment
        fields = ['client', 'repairnum', 'specnum', 'eq', 'eq_p', 'eq_u', 'eq_n', 'winding_time', 'assembly_time']


class ScopeShipmentTransformersFilter(django_filters.FilterSet):
    client = django_filters.ModelChoiceFilter(label=u'Контрагент', queryset=Client.objects.all(),
                                              field_name="shipment__client")
    specnum = django_filters.CharFilter(label=u'Номер спецификации', field_name="shipment__specificationnum",
                                        lookup_expr='icontains')
    eq_unn = django_filters.NumberFilter(label=u'Unn', field_name="equipment__unn")
    eq_uvn = django_filters.NumberFilter(label=u'Uvn', field_name="equipment__uvn")

    class Meta:
        model = ScopeShipment
        fields = ['client', 'repairnum', 'specnum', 'eq_unn', 'eq_uvn']


class ParamsRenovationObject(models.Model):
    equipment = models.ForeignKey(ScopeShipment, on_delete=models.CASCADE)
    part = models.ForeignKey(Parts, verbose_name=u'Наименование', on_delete=models.CASCADE)
    availability = models.BooleanField(u'В наличии', default=True)

    def __str__(self):
        return self.part.name

    class Meta:
        verbose_name = u'Деталь оборудования'
        verbose_name_plural = u'Состав оборудования'


# Комментарии
class Comments(models.Model):
    equipment = models.ForeignKey(ScopeShipment, on_delete=models.CASCADE)
    text = models.TextField(u'Комментарий', blank=True)

    datetime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    create_user = CurrentUserField(on_update=False)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = u'Комментарий'
        verbose_name_plural = u'Комментарии'


class Photos(models.Model):
    equipment = models.ForeignKey(ScopeShipment, on_delete=models.CASCADE)
    photo = models.ImageField(u'Фото', upload_to='repairshop/', blank=True, null=True)

    datetime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    create_user = CurrentUserField(on_update=False)

    def __str__(self):
        return self.photo.name

    class Meta:
        verbose_name = u'Фото'
        verbose_name_plural = u'Фотографии РН'


# Разборка
class Disassembly(models.Model):
    equipment = models.ForeignKey(ScopeShipment, on_delete=models.CASCADE)

    name = models.CharField(u'Наименование работ', max_length=100, blank=True, null=True)
    comment = models.CharField(u'Замечание', max_length=100, blank=True, null=True)

    executor = models.ManyToManyField(Profile, verbose_name=u'Исполнитель', blank=True, related_name='ds_executor')
    date_due = models.DateField(u'Срок выполнения', blank=True, null=True)
    complete = models.BooleanField(u'Выполнено', default=False, blank=True)
    date_complete = models.DateTimeField(u'Дата выполнения', blank=True, null=True)

    group_receiving = models.ForeignKey(Group, verbose_name=u'Ответственная группа', blank=True, null=True,
                                        related_name='ds_group_receiving', on_delete=models.CASCADE)
    accepted = models.BooleanField(u'Принято', blank=True, default=False)
    receiving = models.ForeignKey(Profile, verbose_name=u'Принял', blank=True, null=True,
                                  related_name='ds_receiving', on_delete=models.CASCADE)
    date_receiving = models.DateTimeField(u'Дата принятия', blank=True, null=True)
    images = models.ManyToManyField(Photos, verbose_name=u'Исполнитель', blank=True, related_name='ds_images')

    create_user = CurrentUserField(related_name='ds_create_user', on_update=False)
    update_user = CurrentUserField(related_name='ds_update_user', on_update=True)

    datetime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    datetime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Позиция'
        verbose_name_plural = u'Разборка'


# Дефектовка
class FaultDetection(models.Model):
    equipment = models.ForeignKey(ScopeShipment, on_delete=models.CASCADE)

    name = models.CharField(u'Наименование работ', max_length=100, blank=True, null=True)
    price = models.DecimalField(u'Стоимость позиции', decimal_places=2, max_digits=8, blank=True, null=True)
    general_info = models.CharField(u'Общие сведения', max_length=100, blank=True, null=True)
    type_work = models.CharField(u'Вид работ', max_length=100, blank=True, null=True)
    count_components = models.IntegerField(u'Количество по конструкции', blank=True, null=True)
    count_order = models.IntegerField(u'Заказ', blank=True, null=True)

    executor = models.ManyToManyField(Profile, verbose_name=u'Исполнитель', blank=True, related_name='fd_executor')
    date_due = models.DateField(u'Срок выполнения', blank=True, null=True)
    complete = models.BooleanField(u'Выполнено', default=False)
    date_complete = models.DateTimeField(u'Дата выполнения', blank=True, null=True)

    group_receiving = models.ForeignKey(Group, verbose_name=u'Ответственная группа', blank=True, null=True,
                                        related_name='fd_group_receiving', on_delete=models.CASCADE)
    result = models.ForeignKey(ResultsDetailTechProcess, verbose_name=u'Результат',
                               blank=True, null=True, on_delete=models.CASCADE)
    receiving = models.ForeignKey(Profile, verbose_name=u'Принял', blank=True, null=True,
                                  related_name='fd_receiving', on_delete=models.CASCADE)
    date_receiving = models.DateTimeField(u'Дата принятия', blank=True, null=True)

    create_user = CurrentUserField(related_name='fd_create_user', on_update=False)
    update_user = CurrentUserField(related_name='fd_update_user', on_update=True)

    datetime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    datetime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Позиция'
        verbose_name_plural = u'Дефектовка'


# Механика
class Mechanics(models.Model):
    equipment = models.ForeignKey(ScopeShipment, on_delete=models.CASCADE)

    name = models.CharField(u'Наименование', max_length=100, blank=True, null=True)
    price = models.DecimalField(u'Стоимость позиции', decimal_places=2, max_digits=8, blank=True, null=True)
    degrees_0 = models.CharField(u'0', max_length=100, blank=True, null=True)
    degrees_120 = models.CharField(u'120', max_length=100, blank=True, null=True)
    degrees_240 = models.CharField(u'240', max_length=100, blank=True, null=True)
    seat_diameter = models.DecimalField(u'Диаметр посадочного места', decimal_places=2,
                                        max_digits=5, blank=True, null=True)
    material = models.ForeignKey(Material, verbose_name=u'Материал', blank=True, null=True, on_delete=models.CASCADE)
    comment = models.CharField(u'Замечание', max_length=100, blank=True, null=True)

    executor = models.ManyToManyField(Profile, verbose_name=u'Исполнитель', blank=True, related_name='m_executor')
    date_due = models.DateField(u'Срок выполнения', blank=True, null=True)
    complete = models.BooleanField(u'Выполнено', default=False)
    date_complete = models.DateTimeField(u'Дата выполнения', blank=True, null=True)

    group_receiving = models.ForeignKey(Group, verbose_name=u'Ответственная группа', blank=True, null=True,
                                        related_name='m_group_receiving', on_delete=models.CASCADE)
    receiving = models.ForeignKey(Profile, verbose_name=u'Принял', blank=True, null=True,
                                  related_name='m_receiving', on_delete=models.CASCADE)
    result = models.ForeignKey(ResultsDetailTechProcess, verbose_name=u'Результат',
                               blank=True, null=True, on_delete=models.CASCADE)
    date_receiving = models.DateTimeField(u'Дата принятия', blank=True, null=True)

    create_user = CurrentUserField(related_name='m_create_user', on_update=False)
    update_user = CurrentUserField(related_name='m_update_user', on_update=True)

    datetime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    datetime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Позиция'
        verbose_name_plural = u'Механика'


# Испытание
class Tests(models.Model):
    equipment = models.ForeignKey(ScopeShipment, on_delete=models.CASCADE)

    indications = models.CharField(u'Показания', max_length=100, blank=True, null=True)
    stator = models.CharField(u'Статор', max_length=100, blank=True, null=True)
    rotor_cage = models.CharField(u'Беличья клетка ротора (литой, сварной)', max_length=100, blank=True, null=True)
    rings = models.CharField(u'Токосъёмные кольца', max_length=100, blank=True, null=True)

    executor = models.ManyToManyField(Profile, verbose_name=u'Исполнитель', blank=True, related_name='t_executor')
    date_due = models.DateField(u'Срок выполнения', blank=True, null=True)
    complete = models.BooleanField(u'Выполнено', default=False)
    date_complete = models.DateTimeField(u'Дата выполнения', blank=True, null=True)

    create_user = CurrentUserField(related_name='t_create_user', on_update=False)
    update_user = CurrentUserField(related_name='t_update_user', on_update=True)

    datetime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    datetime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    def __str__(self):
        return self.indications

    class Meta:
        verbose_name = u'Позиция'
        verbose_name_plural = u'Испытание'


# Склад
class Storage(models.Model):
    equipment = models.ForeignKey(ScopeShipment, on_delete=models.CASCADE)

    detail = models.ForeignKey(Parts, verbose_name=u'Запчасть', blank=True, null=True, on_delete=models.CASCADE)
    date_record = models.DateField(u'Дата записи', blank=True, null=True)
    count_details = models.IntegerField(u'Количество', blank=True, null=True)
    date_order = models.DateField(u'Дата заказа', blank=True, null=True)
    status_availability = models.ForeignKey(StatusAvailability, verbose_name=u'Статус', blank=True, null=True,
                                            on_delete=models.CASCADE)
    comment = models.CharField(u'Замечание', max_length=100, blank=True, null=True)
    
    create_user = CurrentUserField(related_name='st_create_user', on_update=False)
    update_user = CurrentUserField(related_name='st_update_user', on_update=True)

    datetime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    datetime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    def __str__(self):
        return self.detail.name

    class Meta:
        verbose_name = u'Позиция'
        verbose_name_plural = u'Склад'


Detail = (
    ('poles', 'Полюса'),
    ('sections', 'Секции'),
    ('inductor', 'Индуктор'),
    ('anchor', 'Якорь'),
    ('shields', 'Щиты'),
    ('spindle', 'Вал')
)

Stage = (
    ('inwinding', 'в намотку'),
    ('tobelaid', 'к укладке'),
    ('onassembly', 'на сборку')
)


# Полюса
class Poles(models.Model):
    equipment = models.ForeignKey(ScopeShipment, on_delete=models.CASCADE)

    name = models.CharField(u'Наименование', max_length=100, blank=True, null=True)
    price = models.DecimalField(u'Стоимость', decimal_places=2, max_digits=8, blank=True, null=True)
    count_plan = models.IntegerField(u'Количество план', blank=True, null=True)
    count_fact = models.IntegerField(u'Количество факт', blank=True, null=True)

    date_due = models.DateField(u'Срок выполнения', blank=True, null=True)
    complete = models.BooleanField(u'Выполнено', default=False)
    executor = models.ManyToManyField(Profile, verbose_name=u'Исполнитель', blank=True, related_name='poles_executor')
    date_complete = models.DateField(u'Дата выполнения', blank=True, null=True)

    group_receiving = models.ForeignKey(Group, verbose_name=u'Ответственная группа', blank=True, null=True,
                                        related_name='poles_group_receiving', on_delete=models.CASCADE)
    receiving = models.ForeignKey(Profile, verbose_name=u'Принял', blank=True, null=True,
                                  related_name='poles_receiving', on_delete=models.CASCADE)
    result = models.ForeignKey(ResultsDetailTechProcess, verbose_name=u'Результат', blank=True, null=True,
                               on_delete=models.CASCADE)
    date_receiving = models.DateTimeField(u'Дата принятия', blank=True, null=True)

    comment = models.CharField(u'Замечание', max_length=100, blank=True, null=True)
    
    create_user = CurrentUserField(related_name='poles_create_user', on_update=False)
    update_user = CurrentUserField(related_name='poles_update_user', on_update=True)

    datetime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    datetime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Позиция'
        verbose_name_plural = u'Полюсы'


# Секции
class Sections(models.Model):
    equipment = models.ForeignKey(ScopeShipment, on_delete=models.CASCADE)

    name = models.CharField(u'Наименование', max_length=100, blank=True, null=True)
    price = models.DecimalField(u'Стоимость', decimal_places=2, max_digits=8, blank=True, null=True)
    count_plan = models.IntegerField(u'Количество план', blank=True, null=True)
    count_fact = models.IntegerField(u'Количество факт', blank=True, null=True)

    date_due = models.DateField(u'Срок выполнения', blank=True, null=True)
    complete = models.BooleanField(u'Выполнено', default=False)
    executor = models.ManyToManyField(Profile, verbose_name=u'Исполнитель', blank=True, related_name='sections_executor')
    date_complete = models.DateField(u'Дата выполнения', blank=True, null=True)

    group_receiving = models.ForeignKey(Group, verbose_name=u'Ответственная группа', blank=True, null=True,
                                        related_name='sections_group_receiving', on_delete=models.CASCADE)
    receiving = models.ForeignKey(Profile, verbose_name=u'Принял', blank=True, null=True,
                                  related_name='sections_receiving', on_delete=models.CASCADE)
    result = models.ForeignKey(ResultsDetailTechProcess, verbose_name=u'Результат', blank=True, null=True,
                               on_delete=models.CASCADE)
    date_receiving = models.DateTimeField(u'Дата принятия', blank=True, null=True)

    comment = models.CharField(u'Замечание', max_length=100, blank=True, null=True)

    create_user = CurrentUserField(related_name='sections_create_user', on_update=False)
    update_user = CurrentUserField(related_name='sections_update_user', on_update=True)

    datetime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    datetime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Позиция'
        verbose_name_plural = u'Секции'


# Индуктор
class Inductor(models.Model):
    equipment = models.ForeignKey(ScopeShipment, on_delete=models.CASCADE)

    name = models.CharField(u'Наименование', max_length=100, blank=True, null=True)
    price = models.DecimalField(u'Стоимость', decimal_places=2, max_digits=8, blank=True, null=True)
    count_plan = models.IntegerField(u'Количество план', blank=True, null=True)
    count_fact = models.IntegerField(u'Количество факт', blank=True, null=True)

    date_due = models.DateField(u'Срок выполнения', blank=True, null=True)
    complete = models.BooleanField(u'Выполнено', default=False)
    executor = models.ManyToManyField(Profile, verbose_name=u'Исполнитель', blank=True, related_name='inductor_executor')
    date_complete = models.DateField(u'Дата выполнения', blank=True, null=True)

    group_receiving = models.ForeignKey(Group, verbose_name=u'Ответственная группа', blank=True, null=True,
                                        related_name='inductor_group_receiving', on_delete=models.CASCADE)
    receiving = models.ForeignKey(Profile, verbose_name=u'Принял', blank=True, null=True,
                                  related_name='inductor_receiving', on_delete=models.CASCADE)
    result = models.ForeignKey(ResultsDetailTechProcess, verbose_name=u'Результат', blank=True, null=True,
                               on_delete=models.CASCADE)
    date_receiving = models.DateTimeField(u'Дата принятия', blank=True, null=True)

    comment = models.CharField(u'Замечание', max_length=100, blank=True, null=True)

    create_user = CurrentUserField(related_name='inductor_create_user', on_update=False)
    update_user = CurrentUserField(related_name='inductor_update_user', on_update=True)

    datetime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    datetime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Позиция'
        verbose_name_plural = u'Индуктор'


# Якорь
class Anchor(models.Model):
    equipment = models.ForeignKey(ScopeShipment, on_delete=models.CASCADE)

    name = models.CharField(u'Наименование', max_length=100, blank=True, null=True)
    price = models.DecimalField(u'Стоимость', decimal_places=2, max_digits=8, blank=True, null=True)
    count_plan = models.IntegerField(u'Количество план', blank=True, null=True)
    count_fact = models.IntegerField(u'Количество факт', blank=True, null=True)

    date_due = models.DateField(u'Срок выполнения', blank=True, null=True)
    complete = models.BooleanField(u'Выполнено', default=False)
    executor = models.ManyToManyField(Profile, verbose_name=u'Исполнитель', blank=True, related_name='anchor_executor')
    date_complete = models.DateField(u'Дата выполнения', blank=True, null=True)

    group_receiving = models.ForeignKey(Group, verbose_name=u'Ответственная группа', blank=True, null=True,
                                        related_name='anchor_group_receiving', on_delete=models.CASCADE)
    receiving = models.ForeignKey(Profile, verbose_name=u'Принял', blank=True, null=True,
                                  related_name='anchor_receiving', on_delete=models.CASCADE)
    result = models.ForeignKey(ResultsDetailTechProcess, verbose_name=u'Результат', blank=True, null=True,
                               on_delete=models.CASCADE)
    date_receiving = models.DateTimeField(u'Дата принятия', blank=True, null=True)

    comment = models.CharField(u'Замечание', max_length=100, blank=True, null=True)

    create_user = CurrentUserField(related_name='anchor_create_user', on_update=False)
    update_user = CurrentUserField(related_name='anchor_update_user', on_update=True)

    datetime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    datetime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Позиция'
        verbose_name_plural = u'Якорь'


# Щиты
class Shields(models.Model):
    equipment = models.ForeignKey(ScopeShipment, on_delete=models.CASCADE)

    name = models.CharField(u'Наименование', max_length=100, blank=True, null=True)
    price = models.DecimalField(u'Стоимость', decimal_places=2, max_digits=8, blank=True, null=True)
    count_plan = models.IntegerField(u'Количество план', blank=True, null=True)
    count_fact = models.IntegerField(u'Количество факт', blank=True, null=True)

    date_due = models.DateField(u'Срок выполнения', blank=True, null=True)
    complete = models.BooleanField(u'Выполнено', default=False)
    executor = models.ManyToManyField(Profile, verbose_name=u'Исполнитель', blank=True, related_name='shields_executor')
    date_complete = models.DateField(u'Дата выполнения', blank=True, null=True)

    group_receiving = models.ForeignKey(Group, verbose_name=u'Ответственная группа', blank=True, null=True,
                                        related_name='shields_group_receiving', on_delete=models.CASCADE)
    receiving = models.ForeignKey(Profile, verbose_name=u'Принял', blank=True, null=True,
                                  related_name='shields_receiving', on_delete=models.CASCADE)
    result = models.ForeignKey(ResultsDetailTechProcess, verbose_name=u'Результат', blank=True, null=True,
                               on_delete=models.CASCADE)
    date_receiving = models.DateTimeField(u'Дата принятия', blank=True, null=True)

    comment = models.CharField(u'Замечание', max_length=100, blank=True, null=True)

    create_user = CurrentUserField(related_name='shields_create_user', on_update=False)
    update_user = CurrentUserField(related_name='shields_update_user', on_update=True)

    datetime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    datetime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Позиция'
        verbose_name_plural = u'Щиты'


# Вал
class Spindle(models.Model):
    equipment = models.ForeignKey(ScopeShipment, on_delete=models.CASCADE)

    name = models.CharField(u'Наименование', max_length=100, blank=True, null=True)
    price = models.DecimalField(u'Стоимость', decimal_places=2, max_digits=8, blank=True, null=True)
    count_plan = models.IntegerField(u'Количество план', blank=True, null=True)
    count_fact = models.IntegerField(u'Количество факт', blank=True, null=True)

    date_due = models.DateField(u'Срок выполнения', blank=True, null=True)
    complete = models.BooleanField(u'Выполнено', default=False)
    executor = models.ManyToManyField(Profile, verbose_name=u'Исполнитель', blank=True, related_name='spindle_executor')
    date_complete = models.DateField(u'Дата выполнения', blank=True, null=True)

    group_receiving = models.ForeignKey(Group, verbose_name=u'Ответственная группа', blank=True, null=True,
                                        related_name='spindle_group_receiving', on_delete=models.CASCADE)
    receiving = models.ForeignKey(Profile, verbose_name=u'Принял', blank=True, null=True,
                                  related_name='spindle_receiving', on_delete=models.CASCADE)
    result = models.ForeignKey(ResultsDetailTechProcess, verbose_name=u'Результат', blank=True, null=True,
                               on_delete=models.CASCADE)
    date_receiving = models.DateTimeField(u'Дата принятия', blank=True, null=True)

    comment = models.CharField(u'Замечание', max_length=100, blank=True, null=True)

    create_user = CurrentUserField(related_name='spindle_create_user', on_update=False)
    update_user = CurrentUserField(related_name='spindle_update_user', on_update=True)

    datetime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    datetime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Позиция'
        verbose_name_plural = u'Вал'


# Комплектующие
class Completing(models.Model):
    equipment = models.ForeignKey(ScopeShipment, on_delete=models.CASCADE)

    name = models.CharField(u'Наименование', max_length=100, blank=True, null=True)
    price = models.DecimalField(u'Стоимость', decimal_places=2, max_digits=8, blank=True, null=True)
    count_plan = models.IntegerField(u'Количество план', blank=True, null=True)
    count_fact = models.IntegerField(u'Количество факт', blank=True, null=True)

    date_due = models.DateField(u'Срок выполнения', blank=True, null=True)
    complete = models.BooleanField(u'Выполнено', default=False)
    executor = models.ManyToManyField(Profile, verbose_name=u'Исполнитель', blank=True, related_name='cmp_executor')
    date_complete = models.DateField(u'Дата выполнения', blank=True, null=True)

    group_receiving = models.ForeignKey(Group, verbose_name=u'Ответственная группа', blank=True, null=True,
                                        related_name='cmp_group_receiving', on_delete=models.CASCADE)
    receiving = models.ForeignKey(Profile, verbose_name=u'Принял', blank=True, null=True,
                                  related_name='cmp_receiving', on_delete=models.CASCADE)
    result = models.ForeignKey(ResultsDetailTechProcess, verbose_name=u'Результат', blank=True, null=True,
                               on_delete=models.CASCADE)
    date_receiving = models.DateTimeField(u'Дата принятия', blank=True, null=True)

    comment = models.CharField(u'Замечание', max_length=100, blank=True, null=True)

    create_user = CurrentUserField(related_name='cmp_create_user', on_update=False)
    update_user = CurrentUserField(related_name='cmp_update_user', on_update=True)

    datetime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    datetime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Позиция'
        verbose_name_plural = u'Комплектующие'


# Сборка
class Assembly(models.Model):
    equipment = models.ForeignKey(ScopeShipment, on_delete=models.CASCADE)

    name = models.CharField(u'Наименование', max_length=100, blank=True, null=True)
    price = models.DecimalField(u'Стоимость', decimal_places=2, max_digits=8, blank=True, null=True)
    count_plan = models.IntegerField(u'Количество план', blank=True, null=True)
    count_fact = models.IntegerField(u'Количество факт', blank=True, null=True)

    date_due = models.DateField(u'Срок выполнения', blank=True, null=True)
    complete = models.BooleanField(u'Выполнено', default=False)
    executor = models.ManyToManyField(Profile, verbose_name=u'Исполнитель', blank=True, related_name='as_executor')
    date_complete = models.DateField(u'Дата выполнения', blank=True, null=True)

    group_receiving = models.ForeignKey(Group, verbose_name=u'Ответственная группа', blank=True, null=True,
                                        related_name='as_group_receiving', on_delete=models.CASCADE)
    receiving = models.ForeignKey(Profile, verbose_name=u'Принял', blank=True, null=True,
                                  related_name='as_receiving', on_delete=models.CASCADE)
    result = models.ForeignKey(ResultsDetailTechProcess, verbose_name=u'Результат', blank=True, null=True,
                               on_delete=models.CASCADE)
    date_receiving = models.DateTimeField(u'Дата принятия', blank=True, null=True)

    comment = models.CharField(u'Замечание', max_length=100, blank=True, null=True)

    create_user = CurrentUserField(related_name='as_create_user', on_update=False)
    update_user = CurrentUserField(related_name='as_update_user', on_update=True)

    datetime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    datetime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Позиция'
        verbose_name_plural = u'Сборка'


# Вложения
class Investments(models.Model):
    equipment = models.ForeignKey(ScopeShipment, on_delete=models.CASCADE)
    key = models.CharField(u'Код', max_length=30, blank=True, null=True)
    file = models.FileField(u'Файл', upload_to='repairshop/investments/', blank=True, null=True)
    comment = models.CharField(u'Замечание', max_length=100, blank=True, null=True)

    create_user = CurrentUserField(related_name='inv_create_user', on_update=False)
    update_user = CurrentUserField(related_name='inv_update_user', on_update=True)

    datetime_add = models.DateTimeField(u'Дата и время добавления', auto_now_add=True)
    datetime_update = models.DateTimeField(u'Дата и время обновления', auto_now=True)
    
    def __str__(self):
        return str(self.key)

    class Meta:
        verbose_name = u'Позиция'
        verbose_name_plural = u'Вложения'
