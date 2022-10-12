from django.contrib.auth.models import User, Group
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


# Месяца
class MonthList(models.Model):
    name = models.CharField(u'Наименование', max_length=15)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Месяц '
        verbose_name_plural = u'Месяца '


# Города нахождения
class City(models.Model):
    name = models.CharField(u'Город', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Город '
        verbose_name_plural = u'Список городов '


# Филиалы
class Branches(models.Model):
    name = models.CharField(u'Наименование', max_length=100)
    city = models.ForeignKey(City, models.SET_NULL, verbose_name=u'Город', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Филиал '
        verbose_name_plural = u'Филиалы концерна '


class TypesClient(models.Model):
    name = models.CharField(u'Наименование', max_length=100)
    slug = models.SlugField(u'алиас')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Тип'
        verbose_name_plural = u'Типы контрагентов '


# Контрагенты
class Client(models.Model):
    type = models.ForeignKey(TypesClient, models.SET_NULL, verbose_name=u'Тип клиента', null=True)
    name = models.CharField(u'Контрагент', max_length=100)
    inn = models.CharField(u'ИНН', max_length=12, blank=True, null=True)
    kpp = models.CharField(u'КПП', max_length=9, blank=True, null=True)
    branch = models.ForeignKey(Branches, verbose_name=u'Филиал', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = u'Контрагент '
        verbose_name_plural = u'Список контрагентов '


# Должности
class Posts(models.Model):
    name = models.CharField(u'Должность', max_length=100)
    slug = models.SlugField(u'алиас')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Должность '
        verbose_name_plural = u'Список должностей '


TypeEquipment = (
    ('engine', 'ЭлДвигатель'),
    ('transformer', 'Трансформатор'),
    ('other', 'Другое'),
)

TypeAmperage = (
    ('steady', 'Постоянный'),
    ('variable', 'Переменный'),
    ('not_applicable', 'не применимо'),
)

Voltage = (
    ('220', '220v'),
    ('380', '380v'),
)

Section = (
    ('upto100kvt', 'До 100 кВт'),
    ('from100kvt', 'От 100 кВт'),
    ('other', 'Прочие'),
)

ClassColorBs4 = (
    ('success', 'Зелёный'),
    ('warning', 'Жёлтый'),
    ('danger', 'Красный'),
)


# Стадии
class StageProduction(models.Model):
    name = models.CharField(u'Наименование', max_length=100)
    slug = models.SlugField(u'Ключ статуса', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Стадия'
        verbose_name_plural = u'Стадии производства '


# Детали
class Parts(models.Model):
    name = models.CharField(u'Наименование', max_length=30)
    typeequipment = models.CharField(u'Тип оборудования', choices=TypeEquipment, max_length=15, blank=True, null=True)
    amperage = models.CharField(u'Тип тока', choices=TypeAmperage, max_length=15, blank=True, null=True)
    mainparts = models.BooleanField(u'Основная деталь', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Деталь'
        verbose_name_plural = u'Детали двигателей/трансформаторов '


# Оборудование
class ModelEquipment(models.Model):
    type = models.CharField(u'Тип оборудования', choices=TypeEquipment, max_length=15)
    amperage = models.CharField(u'Тип тока', choices=TypeAmperage, max_length=15, blank=True, null=True)
    name = models.CharField(u'Наименование', max_length=30)
    p = models.DecimalField(u'Мощность', max_digits=5, decimal_places=1, blank=True, default=0)
    u = models.CharField(u'Напряжение', max_length=50, blank=True, null=True)
    n = models.IntegerField(u'Обороты', blank=True, null=True)
    unn = models.IntegerField(u'Напряжение низкой стороны', blank=True, null=True)
    uvn = models.IntegerField(u'Напряжение высокой стороны', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Модель'
        verbose_name_plural = u'Оборудование '


class UrgencyRepairs(models.Model):
    name = models.CharField(u'Наименование', max_length=50)
    color = models.CharField(u'Цвет уведомления', choices=ClassColorBs4, max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Уровень'
        verbose_name_plural = u'Срочность ремонта '


class SendMailList(models.Model):
    recipient_groups = models.CharField(u'Наименование группы получателей', max_length=100)
    branch = models.ForeignKey(Branches, verbose_name=u'Филиал', on_delete=models.CASCADE)
    subject = models.CharField(u'Тема письма', max_length=100)
    destination = models.ManyToManyField(User, verbose_name='Получатели ',
                                         help_text=u'Выберите получателей уведомлений', max_length=2)
    message = models.TextField(u'Текст письма', help_text=u'В тексте письма обязательно должен находится тег %object%')
    email = models.EmailField(u'Электронный почтовый адрес')

    def __str__(self):
        return self.recipient_groups

    class Meta:
        verbose_name = u'Получатель '
        verbose_name_plural = u'Список рассылки уведомлений '


class StatusWork(models.Model):
    name = models.CharField(u'Состояние', max_length=100)
    slug = models.SlugField(u'Ключ статуса', unique=True)
    tr_color = models.CharField(u'Цвет строки', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Статус '
        verbose_name_plural = u'Статусы заявок '


class StatusAvailability(models.Model):
    name = models.CharField(u'Состояние', max_length=100)
    slug = models.SlugField(u'Ключ статуса', unique=True)
    tr_color = models.CharField(u'Цвет строки', max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Статус '
        verbose_name_plural = u'Статусы наличия '


class StatusTask(models.Model):
    name = models.CharField(u'Состояние', max_length=100)
    slug = models.SlugField(u'Ключ статуса', unique=True)
    class_b4 = models.CharField(u'Цвет строки', max_length=50, blank=True, null=True,
                                help_text=u'Классы: active, primary, secondary, success, '
                                          u'danger, warning, info, light, dark')
    view_list = models.BooleanField(u'Выводить в список', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Статус '
        verbose_name_plural = u'Статусы задач '


class StatusReceiving(models.Model):
    name = models.CharField(u'Состояние', max_length=100)
    slug = models.SlugField(u'Ключ статуса', unique=True)
    class_b4 = models.CharField(u'Цвет строки', max_length=50, blank=True, null=True,
                                help_text=u'Классы: active, primary, secondary, success, '
                                          u'danger, warning, info, light, dark')
    view_list = models.BooleanField(u'Выводить в список', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Статус '
        verbose_name_plural = u'Статусы контроля '


class TypeNotificationTask(models.Model):
    name = models.CharField(u'Состояние', max_length=100)
    slug = models.SlugField(u'Ключ статуса', unique=True)
    color = models.CharField(u'Цвет строки', max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Тип '
        verbose_name_plural = u'Варианты уведомления '


# Допуски валов
class ShaftTolerances(models.Model):
    d1 = models.IntegerField(u'Диаметр 1')
    d2 = models.IntegerField(u'Диаметр 2')
    deviation_min = models.DecimalField(u'Отклонение минимальное', max_digits=5, decimal_places=4)
    deviation_max = models.DecimalField(u'Отклонение максимальное', max_digits=5, decimal_places=4)

    def __str__(self):
        return str(self.d1) + '/' + str(self.d2)

    class Meta:
        verbose_name = u'Вал'
        verbose_name_plural = u'Допуски валов '


TechProcess = (
    ('disassembly', 'Разборка'),
    ('faultdetection', 'Дефектация'),
    ('mechanics', 'Механика'),
    ('tests', 'Испытания'),
    ('poles', 'Полюса'),
    ('sections', 'Секции'),
    ('inductor&stator', 'Индуктор/Статор'),
    ('rotor&anchor', 'Якорь/Ротор'),
    ('shields', 'Щиты'),
    ('spindle', 'Вал'),
    ('completing', 'Комплектующие'),
    ('assembly', 'Сборка'),
)


# Детали техпроцесса
class ResultsDetailTechProcess(models.Model):
    name = models.CharField(u'Наименование', max_length=50)
    slug = models.SlugField(u'Алиас', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Результат'
        verbose_name_plural = u'Результаты единицы техпроцесса'


# Дерево техпроцесса
class TreeTechProcess(MPTTModel):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('Ключ категории', blank=True, null=True)
    responsible_group = models.ForeignKey(Group, models.SET_NULL, verbose_name='Группа ответственных', blank=True, null=True)
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name="Родитель",
                            related_name='child', db_index=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Ветка '
        verbose_name_plural = u'Дерево техпроцесса '

    class MPTTMeta:
        level_attr = 'mptt_level'


# Стадии техпроцесса
class TreeTechProcessStage(MPTTModel):
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('Ключ категории', blank=True, null=True)
    parent = TreeForeignKey('self', blank=True, null=True, verbose_name="Родитель",
                            related_name='child', db_index=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Стадия '
        verbose_name_plural = u'Стадии техпроцессов '

    class MPTTMeta:
        level_attr = 'mptt_level'


# Материалы
class Material(models.Model):
    name = models.CharField(u'Наименование', max_length=50)
    slug = models.SlugField(u'Алиас', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'Материал'
        verbose_name_plural = u'Материалы'
