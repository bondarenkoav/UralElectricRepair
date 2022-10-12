from django import forms
from django.contrib.auth.models import User, Group
from django_currentuser.middleware import get_current_user
from upload_validator import FileTypeValidator
from django.forms import modelformset_factory

from accounts.models import Profile
from accounts.views import get_cur_branch
from reference_books.models import ModelEquipment, Client, TreeTechProcess, TreeTechProcessStage
from repairfund.widgets import ListTextWidget
from repairshop.models import Shipment, ScopeShipment, FaultDetection, Mechanics, Tests, Storage, \
    Poles, Sections, Inductor, Anchor, Shields, Spindle, Investments, Disassembly, Completing, Assembly, Comments


# Форма добавления поставки
class FormAddShipment(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(FormAddShipment, self).__init__(*args, **kwargs)

        self.fields['client'].widget = ListTextWidget(
            data_list=Client.objects.filter(branch=get_cur_branch()).
                values_list('name', flat=True).order_by('name'), name='client-list')

    client = forms.CharField(label='Контрагент', required=True)
    dateshipment = forms.DateField(required=False, label=u'Дата поставки',
                                   widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                   input_formats=('%Y-%m-%d',))
    photo = forms.ImageField(label=u'Фото поставки', required=True,
                             validators=[FileTypeValidator(allowed_types=['image/jpeg', 'image/jpg', 'image/png'])])

    def clean(self):
        cleaned_data = super(FormAddShipment, self).clean()

        if not self.errors:
            client = cleaned_data['client']
            try:
                cleaned_data['client'], created = Client.objects.update_or_create(
                    name=client, defaults={'name': client, 'branch': get_cur_branch()}
                )
            except:
                raise forms.ValidationError(u'Вашему профилю не назначены филиалы. Обратитесь к админристратору.')

        return cleaned_data

    class Meta:
        model = Shipment
        fields = ['specificationnum', 'client', 'dateshipment', 'photo']


GroupsEquipment = (
    ('engines_variable', 'Эл.двигатели переменного тока'),
    ('engines_steady', 'Эл.двигатели постоянного тока'),
    ('engines_upto100kvt', 'Эл.двигатели до 10кВт'),
    ('transformer', 'Трансформаторы'),
    ('other', 'Другие'),
)


def convert_queryset_to_dict():
    query = ModelEquipment.objects.all()
    list_result = [entry for entry in query]
    return list_result


# Форма ввода состава поставки
class FormAddScopeShipment(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormAddScopeShipment, self).__init__(*args, **kwargs)

        self.fields['equipment'].widget = ListTextWidget(
            data_list=ModelEquipment.objects.values_list('name', flat=True).order_by('name'),
            name='equipment-list')

    equipment = forms.CharField(label='Модель оборудования', required=True)
    group_eq = forms.ChoiceField(choices=GroupsEquipment, label=u'Группа оборудования', required=True)
    estimate = forms.BooleanField(label=u'', required=False)

    def clean(self):
        cleaned_data = super(FormAddScopeShipment, self).clean()

        if not self.errors:
            equipment = cleaned_data['equipment']
            group = cleaned_data['group_eq']

            amperage_eq = None
            if group == 'engines_variable':
                type_eq = 'engine'
                amperage_eq = 'variable'
            elif group == 'engines_steady':
                type_eq = 'engine'
                amperage_eq = 'steady'
            elif group == 'engines_upto100kvt':
                type_eq = 'engine'
            else:
                type_eq = group
                amperage_eq = 'not_applicable'
            eq_model, created = ModelEquipment.objects.update_or_create(
                name=equipment, defaults={'name': equipment, 'type': type_eq, 'amperage': amperage_eq})
            cleaned_data['equipment'] = eq_model

        return cleaned_data

    class Meta:
        model = ScopeShipment
        fields = ['repairnum', 'equipment', 'group_eq', 'urgency', 'section', 'estimate']


ScopeShipmentFormSet = modelformset_factory(ScopeShipment, form=FormAddScopeShipment, min_num=5, extra=1)


# Форма ввода характеристик оборудования
class FormAddCharactEquipment(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormAddCharactEquipment, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

    class Meta:
        model = ModelEquipment
        fields = '__all__'


CharactEquipmentFormSet = modelformset_factory(ModelEquipment, form=FormAddCharactEquipment, extra=0)


class ScopeShipmentUpdateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ScopeShipmentUpdateForm, self).__init__(*args, **kwargs)
        self.fields['equipment'].widget = forms.HiddenInput()

    comment = forms.CharField(required=False, label=u'Комментарий')

    disassembly_time = forms.DateField(required=False, label=u'Срок',
                                       widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                       input_formats=('%Y-%m-%d',))
    faultdetection_time = forms.DateField(required=False, label=u'Срок',
                                          widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                          input_formats=('%Y-%m-%d',))
    storage_time = forms.DateField(required=False, label=u'Срок',
                                   widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                   input_formats=('%Y-%m-%d',))
    poles_time = forms.DateField(required=False, label=u'Срок',
                                 widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                 input_formats=('%Y-%m-%d',))
    sections_time = forms.DateField(required=False, label=u'Срок',
                                    widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                    input_formats=('%Y-%m-%d',))
    inductor_time = forms.DateField(required=False, label=u'Срок',
                                    widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                    input_formats=('%Y-%m-%d',))
    anchor_time = forms.DateField(required=False, label=u'Срок якорь',
                                  widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                  input_formats=('%Y-%m-%d',))
    shields_time = forms.DateField(required=False, label=u'Срок',
                                   widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                   input_formats=('%Y-%m-%d',))
    spindle_time = forms.DateField(required=False, label=u'Срок',
                                   widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                   input_formats=('%Y-%m-%d',))
    completing_time = forms.DateField(required=False, label=u'Срок',
                                      widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                      input_formats=('%Y-%m-%d',))
    assembly_time = forms.DateField(required=False, label=u'Срок',
                                    widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                    input_formats=('%Y-%m-%d',))
    conservation_time = forms.DateField(required=False, label=u'Срок',
                                        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                        input_formats=('%Y-%m-%d',))

    faultdetection_tpl = forms.ModelChoiceField(required=False, label=u'Шаблон',
                                                queryset=TreeTechProcess.objects.get(slug='faultdetection').get_children(),
                                                widget=forms.Select())
    mechanics_tpl = forms.ModelChoiceField(required=False, label=u'Шаблон',
                                           queryset=TreeTechProcess.objects.get(slug='mechanics').get_children(),
                                           widget=forms.Select())
    tests_tpl = forms.ModelChoiceField(required=False, label=u'Шаблон',
                                       queryset=TreeTechProcess.objects.get(slug='tests').get_children(),
                                       widget=forms.Select())
    poles_tpl = forms.ModelChoiceField(required=False, label=u'Шаблон',
                                       queryset=TreeTechProcess.objects.get(slug='poles').get_children(),
                                       widget=forms.Select())
    sections_tpl = forms.ModelChoiceField(required=False, label=u'Шаблон',
                                          queryset=TreeTechProcess.objects.get(slug='sections').get_children(),
                                          widget=forms.Select())
    inductor_tpl = forms.ModelChoiceField(required=False, label=u'Шаблон',
                                          queryset=TreeTechProcess.objects.get(slug='inductor').get_children(),
                                          widget=forms.Select())
    anchor_tpl = forms.ModelChoiceField(required=False, label=u'Шаблон',
                                        queryset=TreeTechProcess.objects.get(slug='anchor').get_children(),
                                        widget=forms.Select())
    shields_tpl = forms.ModelChoiceField(required=False, label=u'Шаблон',
                                         queryset=TreeTechProcess.objects.get(slug='shields').get_children(),
                                         widget=forms.Select())
    spindle_tpl = forms.ModelChoiceField(required=False, label=u'Шаблон',
                                         queryset=TreeTechProcess.objects.get(slug='spindle').get_children(),
                                         widget=forms.Select())
    completing_tpl = forms.ModelChoiceField(required=False, label=u'Шаблон',
                                            queryset=TreeTechProcess.objects.get(slug='completing').get_children(),
                                            widget=forms.Select())
    assembly_tpl = forms.ModelChoiceField(required=False, label=u'Шаблон',
                                          queryset=TreeTechProcess.objects.get(slug='assembly').get_children(),
                                          widget=forms.Select())

    stage_poles = forms.ModelChoiceField(required=False, label=u'Стадия', widget=forms.Select(),
                                         queryset=TreeTechProcessStage.objects.get(slug='poles').get_children())
    stage_sections = forms.ModelChoiceField(required=False, label=u'Стадия', widget=forms.Select(),
                                            queryset=TreeTechProcessStage.objects.get(slug='sections').get_children())
    stage_inductor = forms.ModelChoiceField(required=False, label=u'Стадия', widget=forms.Select(),
                                            queryset=TreeTechProcessStage.objects.get(slug='inductor').get_children())
    stage_anchor = forms.ModelChoiceField(required=False, label=u'Стадия', widget=forms.Select(),
                                          queryset=TreeTechProcessStage.objects.get(slug='anchor').get_children())
    stage_shields = forms.ModelChoiceField(required=False, label=u'Стадия', widget=forms.Select(),
                                           queryset=TreeTechProcessStage.objects.get(slug='shields').get_children())
    stage_spindle = forms.ModelChoiceField(required=False, label=u'Стадия', widget=forms.Select(),
                                           queryset=TreeTechProcessStage.objects.get(slug='spindle').get_children())

    complete_disassembly = forms.BooleanField(required=False, label='Все работы выполнены и приняты')
    complete_faultdetection = forms.BooleanField(required=False, label='Все работы выполнены и приняты')
    complete_mechanics = forms.BooleanField(required=False, label='Все работы выполнены и приняты')
    complete_tests = forms.BooleanField(required=False, label='Все работы выполнены и приняты')

    complete_poles = forms.BooleanField(required=False, label='Все работы выполнены и приняты')
    complete_sections = forms.BooleanField(required=False, label='Все работы выполнены и приняты')
    complete_inductor = forms.BooleanField(required=False, label='Все работы выполнены и приняты')
    complete_anchor = forms.BooleanField(required=False, label='Все работы выполнены и приняты')
    complete_shields = forms.BooleanField(required=False, label='Все работы выполнены и приняты')
    complete_spindle = forms.BooleanField(required=False, label='Все работы выполнены и приняты')

    complete_completing = forms.BooleanField(required=False, label='Все работы выполнены и приняты')
    complete_assembly = forms.BooleanField(required=False, label='Все работы выполнены и приняты')

    class Meta:
        model = ScopeShipment
        fields = ['equipment', 'section', 'urgency', 'estimate', 'status', 'order', 'archive',
                  'disassembly_time', 'faultdetection_time', 'storage_time',
                  'poles_time', 'sections_time', 'inductor_time', 'anchor_time', 'shields_time', 'spindle_time',
                  'completing_time', 'assembly_time', 'conservation_time',
                  'complete_disassembly', 'complete_faultdetection', 'complete_mechanics', 'complete_tests',
                  'complete_poles', 'complete_sections', 'complete_inductor', 'complete_anchor', 'complete_shields',
                  'complete_spindle', 'complete_completing', 'complete_assembly']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'id': 'post-text',
                'required': False,
                'placeholder': 'Скажите что-то...'
            }),
        }


class DisassemblyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DisassemblyForm, self).__init__(*args, **kwargs)
        branches = Profile.objects.get(user=get_current_user()).branch.all()
        self.fields['executor'].queryset = Profile.objects.filter(
            user__in=User.objects.filter(groups__in=Group.objects.filter(name__in=['КИС', 'Обмотка'])),
            branch__in=branches)
        self.fields['receiving'].queryset = Profile.objects.filter(user__in=User.objects.filter(
            groups__in=Group.objects.filter(name__in=['Ответственные'])),
            branch__in=branches)

    name = forms.CharField(required=True, label='Наименование работ')
    date_due = forms.DateField(required=False, label=u'Срок',
                               widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                               input_formats=('%Y-%m-%d',))
    date_complete = forms.DateField(required=False, label=u'Дата',
                                    widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                    input_formats=('%Y-%m-%d',))
    receiving = forms.ModelChoiceField(required=False, label='Принято', widget=forms.Select(),
                                       queryset=Profile.objects.all())
    executor = forms.ModelMultipleChoiceField(required=False, label='Исполнитель', queryset=Profile.objects.all(),
                                              widget=forms.SelectMultiple(attrs={'class': 'multi_select'}))

    class Meta:
        model = Disassembly
        exclude = ()


DisassemblyFormSet = modelformset_factory(Disassembly, form=DisassemblyForm,
                                          fields=['name', 'executor', 'receiving', 'date_due', 'comment'],
                                          extra=1, can_delete=True)


class FaultDetectionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(FaultDetectionForm, self).__init__(*args, **kwargs)
        branches = Profile.objects.get(user=get_current_user()).branch.all()
        self.fields['executor'].queryset = Profile.objects.filter(
            user__in=User.objects.filter(groups__in=Group.objects.filter(name__in=['КИС', 'Обмотка'])),
            branch__in=branches)
        self.fields['receiving'].queryset = Profile.objects.filter(user__in=User.objects.filter(
            groups__in=Group.objects.filter(name__in=['Ответственные'])),
            branch__in=branches)
        #self.fields['group_receiving'].queryset = Group.objects.filter(name__in=['ОТК', 'ИТР'])

    name = forms.CharField(label='Наименование работ', required=True)
    count_components = forms.IntegerField(label=u'Кол-во деталей', required=False)
    date_due = forms.DateField(required=False, label=u'Срок',
                               widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                               input_formats=('%Y-%m-%d',))
    date_complete = forms.DateField(required=False, label=u'Дата',
                                    widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                    input_formats=('%Y-%m-%d',))
    executor = forms.ModelMultipleChoiceField(required=False, label='Исполнитель', queryset=Profile.objects.all(),
                                              widget=forms.SelectMultiple(attrs={'multiple': 'multiple',
                                                                                 'class': 'multi_select'}))

    class Meta:
        model = FaultDetection
        exclude = ()


FaultDetectionFormSet = modelformset_factory(FaultDetection, form=FaultDetectionForm,
                                             fields=['name', 'general_info', 'type_work', 'count_components',
                                                     'count_order', 'executor', 'receiving', 'receiving', 'date_due'],
                                             extra=1, can_delete=True)


class MechanicsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MechanicsForm, self).__init__(*args, **kwargs)
        branches = Profile.objects.get(user=get_current_user()).branch.all()
        self.fields['executor'].queryset = Profile.objects.filter(
            user__in=User.objects.filter(groups__in=Group.objects.filter(name__in=['КИС', 'Обмотка'])),
            branch__in=branches)
        self.fields['receiving'].queryset = Profile.objects.filter(user__in=User.objects.filter(
            groups__in=Group.objects.filter(name__in=['Ответственные'])),
            branch__in=branches)
        #self.fields['group_receiving'].queryset = Group.objects.filter(name__in=['ОТК', 'ИТР'])

    name = forms.CharField(label='Наименование работ', required=True)
    date_due = forms.DateField(required=False, label=u'Срок',
                               widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                               input_formats=('%Y-%m-%d',))
    executor = forms.ModelMultipleChoiceField(required=False, label='Исполнитель', queryset=Profile.objects.all(),
                                              widget=forms.SelectMultiple(attrs={'multiple': 'multiple',
                                                                                 'class': 'multi_select'}))

    class Meta:
        model = Mechanics
        exclude = ()


MechanicsFormSet = modelformset_factory(Mechanics, form=MechanicsForm,
                                        fields=['name', 'comment', 'degrees_0', 'degrees_120', 'degrees_240',
                                                'receiving', 'seat_diameter', 'material', 'executor', 'date_due'],
                                        extra=1, can_delete=True)


class TestsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TestsForm, self).__init__(*args, **kwargs)
        branches = Profile.objects.get(user=get_current_user()).branch.all()
        self.fields['executor'].queryset = Profile.objects.filter(
            user__in=User.objects.filter(groups__in=Group.objects.filter(name__in=['КИС', 'Обмотка'])),
            branch__in=branches)

    indications = forms.CharField(label='Параметры', required=True)
    date_due = forms.DateField(required=False, label=u'Срок',
                               widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                               input_formats=('%Y-%m-%d',))
    executor = forms.ModelMultipleChoiceField(required=False, label='Исполнитель', queryset=Profile.objects.all(),
                                              widget=forms.SelectMultiple(attrs={'multiple': 'multiple',
                                                                                 'class': 'multi_select'}))

    class Meta:
        model = Tests
        exclude = ()


TestsFormSet = modelformset_factory(Tests, form=TestsForm,
                                    fields=['indications', 'stator', 'rotor_cage', 'rings', 'date_due', 'executor'],
                                    extra=1, can_delete=True)


class StoreForm(forms.ModelForm):
    date_record = forms.DateField(required=False, label=u'Дата',
                                  widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                  input_formats=('%Y-%m-%d',))
    date_order = forms.DateField(required=False, label=u'Дата заказа',
                                 widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                 input_formats=('%Y-%m-%d',))

    class Meta:
        model = Storage
        exclude = ()


StoreFormSet = modelformset_factory(Storage, form=StoreForm,
                                    fields=['date_record', 'detail', 'count_details', 'date_order',
                                            'status_availability', 'comment'], extra=1, can_delete=True)


class PolesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(PolesForm, self).__init__(*args, **kwargs)
        branches = Profile.objects.get(user=get_current_user()).branch.all()
        self.fields['executor'].queryset = Profile.objects.filter(
            user__in=User.objects.filter(groups__in=Group.objects.filter(name__in=['КИС', 'Обмотка'])),
            branch__in=branches)
        self.fields['receiving'].queryset = Profile.objects.filter(user__in=User.objects.filter(
            groups__in=Group.objects.filter(name__in=['Ответственные'])),
            branch__in=branches)
        #self.fields['group_receiving'].queryset = Group.objects.filter(name__in=['ОТК', 'ИТР'])

    name = forms.CharField(label='Наименование работ', required=True)
    complete = forms.BooleanField(label='', required=False)
    date_due = forms.DateField(required=False, label=u'Срок выполнения',
                               widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                               input_formats=('%Y-%m-%d',))
    date_complete = forms.DateField(required=False, label=u'Дата выполнения',
                                    widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                    input_formats=('%Y-%m-%d',))
    date_result = forms.DateField(required=False, label=u'Дата результата',
                                  widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                  input_formats=('%Y-%m-%d',))
    executor = forms.ModelMultipleChoiceField(required=False, label='Исполнитель', queryset=Profile.objects.all(),
                                              widget=forms.SelectMultiple(attrs={'multiple': 'multiple',
                                                                                 'class': 'multi_select'}))

    class Meta:
        model = Poles
        exclude = ()


PolesFormSet = modelformset_factory(Poles, form=PolesForm,
                                    fields=['name', 'date_due', 'executor', 'receiving', 'comment'],
                                    extra=1, can_delete=True)


class SectionsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SectionsForm, self).__init__(*args, **kwargs)
        branches = Profile.objects.get(user=get_current_user()).branch.all()
        self.fields['executor'].queryset = Profile.objects.filter(
            user__in=User.objects.filter(groups__in=Group.objects.filter(name__in=['КИС', 'Обмотка'])),
            branch__in=branches)
        self.fields['receiving'].queryset = Profile.objects.filter(user__in=User.objects.filter(
            groups__in=Group.objects.filter(name__in=['Ответственные'])),
            branch__in=branches)
        #self.fields['group_receiving'].queryset = Group.objects.filter(name__in=['ОТК', 'ИТР'])

    name = forms.CharField(label='Наименование работ', required=True)
    complete = forms.BooleanField(label='', required=False)
    date_due = forms.DateField(required=False, label=u'Срок выполнения',
                               widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                               input_formats=('%Y-%m-%d',))
    date_complete = forms.DateField(required=False, label=u'Дата выполнения',
                                    widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                    input_formats=('%Y-%m-%d',))
    date_result = forms.DateField(required=False, label=u'Дата результата',
                                  widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                  input_formats=('%Y-%m-%d',))
    executor = forms.ModelMultipleChoiceField(required=False, label='Исполнитель', queryset=Profile.objects.all(),
                                              widget=forms.SelectMultiple(attrs={'multiple': 'multiple',
                                                                                 'class': 'multi_select'}))

    class Meta:
        model = Sections
        exclude = ()


SectionsFormSet = modelformset_factory(Sections, form=SectionsForm,
                                       fields=['name', 'date_due', 'executor', 'receiving', 'comment'],
                                       extra=1, can_delete=True)


class InductorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(InductorForm, self).__init__(*args, **kwargs)
        branches = Profile.objects.get(user=get_current_user()).branch.all()
        self.fields['executor'].queryset = Profile.objects.filter(
            user__in=User.objects.filter(groups__in=Group.objects.filter(name__in=['КИС', 'Обмотка'])),
            branch__in=branches)
        self.fields['receiving'].queryset = Profile.objects.filter(user__in=User.objects.filter(
            groups__in=Group.objects.filter(name__in=['Ответственные'])),
            branch__in=branches)
        #self.fields['group_receiving'].queryset = Group.objects.filter(name__in=['ОТК', 'ИТР'])

    name = forms.CharField(label='Наименование работ', required=True)
    complete = forms.BooleanField(label='', required=False)
    date_due = forms.DateField(required=False, label=u'Срок выполнения',
                               widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                               input_formats=('%Y-%m-%d',))
    date_complete = forms.DateField(required=False, label=u'Дата выполнения',
                                    widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                    input_formats=('%Y-%m-%d',))
    date_result = forms.DateField(required=False, label=u'Дата результата',
                                  widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                  input_formats=('%Y-%m-%d',))
    executor = forms.ModelMultipleChoiceField(required=False, label='Исполнитель', queryset=Profile.objects.all(),
                                              widget=forms.SelectMultiple(attrs={'multiple': 'multiple',
                                                                                 'class': 'multi_select'}))

    class Meta:
        model = Inductor
        exclude = ()


InductorFormSet = modelformset_factory(Inductor, form=InductorForm,
                                       fields=['name', 'date_due', 'executor', 'receiving', 'comment'],
                                       extra=1, can_delete=True)


class AnchorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AnchorForm, self).__init__(*args, **kwargs)
        branches = Profile.objects.get(user=get_current_user()).branch.all()
        self.fields['executor'].queryset = Profile.objects.filter(
            user__in=User.objects.filter(groups__in=Group.objects.filter(name__in=['КИС', 'Обмотка'])),
            branch__in=branches)
        self.fields['receiving'].queryset = Profile.objects.filter(user__in=User.objects.filter(
            groups__in=Group.objects.filter(name__in=['Ответственные'])),
            branch__in=branches)
        #self.fields['group_receiving'].queryset = Group.objects.filter(name__in=['ОТК', 'ИТР'])

    name = forms.CharField(label='Наименование работ', required=True)
    complete = forms.BooleanField(label='', required=False)
    date_due = forms.DateField(required=False, label=u'Срок выполнения',
                               widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                               input_formats=('%Y-%m-%d',))
    date_complete = forms.DateField(required=False, label=u'Дата выполнения',
                                    widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                    input_formats=('%Y-%m-%d',))
    date_result = forms.DateField(required=False, label=u'Дата результата',
                                  widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                  input_formats=('%Y-%m-%d',))
    executor = forms.ModelMultipleChoiceField(required=False, label='Исполнитель', queryset=Profile.objects.all(),
                                              widget=forms.SelectMultiple(attrs={'multiple': 'multiple',
                                                                                 'class': 'multi_select'}))

    class Meta:
        model = Anchor
        exclude = ()


AnchorFormSet = modelformset_factory(Anchor, form=AnchorForm,
                                     fields=['name', 'date_due', 'executor', 'receiving', 'comment'],
                                     extra=1, can_delete=True)


class ShieldsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ShieldsForm, self).__init__(*args, **kwargs)
        branches = Profile.objects.get(user=get_current_user()).branch.all()
        self.fields['executor'].queryset = Profile.objects.filter(
            user__in=User.objects.filter(groups__in=Group.objects.filter(name__in=['КИС', 'Обмотка'])),
            branch__in=branches)
        self.fields['receiving'].queryset = Profile.objects.filter(user__in=User.objects.filter(
            groups__in=Group.objects.filter(name__in=['Ответственные'])),
            branch__in=branches)
        #self.fields['group_receiving'].queryset = Group.objects.filter(name__in=['ОТК', 'ИТР'])

    name = forms.CharField(label='Наименование работ', required=True)
    complete = forms.BooleanField(label='', required=False)
    date_due = forms.DateField(required=False, label=u'Срок выполнения',
                               widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                               input_formats=('%Y-%m-%d',))
    date_complete = forms.DateField(required=False, label=u'Дата выполнения',
                                    widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                    input_formats=('%Y-%m-%d',))
    date_result = forms.DateField(required=False, label=u'Дата результата',
                                  widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                  input_formats=('%Y-%m-%d',))
    executor = forms.ModelMultipleChoiceField(required=False, label='Исполнитель', queryset=Profile.objects.all(),
                                              widget=forms.SelectMultiple(attrs={'multiple': 'multiple',
                                                                                 'class': 'multi_select'}))

    class Meta:
        model = Shields
        exclude = ()


ShieldsFormSet = modelformset_factory(Shields, form=ShieldsForm,
                                      fields=['name', 'date_due', 'executor', 'receiving', 'comment'],
                                      extra=1, can_delete=True)


class SpindleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SpindleForm, self).__init__(*args, **kwargs)
        branches = Profile.objects.get(user=get_current_user()).branch.all()
        self.fields['executor'].queryset = Profile.objects.filter(
            user__in=User.objects.filter(groups__in=Group.objects.filter(name__in=['КИС', 'Обмотка'])),
            branch__in=branches)
        self.fields['receiving'].queryset = Profile.objects.filter(user__in=User.objects.filter(
            groups__in=Group.objects.filter(name__in=['Ответственные'])),
            branch__in=branches)
        #self.fields['group_receiving'].queryset = Group.objects.filter(name__in=['ОТК', 'ИТР'])

    name = forms.CharField(label='Наименование работ', required=True)
    complete = forms.BooleanField(label='', required=False)
    date_due = forms.DateField(required=False, label=u'Срок выполнения',
                               widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                               input_formats=('%Y-%m-%d',))
    date_complete = forms.DateField(required=False, label=u'Дата выполнения',
                                    widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                    input_formats=('%Y-%m-%d',))
    date_result = forms.DateField(required=False, label=u'Дата результата',
                                  widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                  input_formats=('%Y-%m-%d',))
    executor = forms.ModelMultipleChoiceField(required=False, label='Исполнитель', queryset=Profile.objects.all(),
                                              widget=forms.SelectMultiple(attrs={'multiple': 'multiple',
                                                                                 'class': 'multi_select'}))

    class Meta:
        model = Spindle
        exclude = ()


SpindleFormSet = modelformset_factory(Spindle, form=SpindleForm,
                                      fields=['name', 'date_due', 'executor', 'receiving', 'comment'],
                                      extra=1, can_delete=True)


class CompletingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CompletingForm, self).__init__(*args, **kwargs)
        branches = Profile.objects.get(user=get_current_user()).branch.all()
        self.fields['executor'].queryset = Profile.objects.filter(
            user__in=User.objects.filter(groups__in=Group.objects.filter(name__in=['КИС', 'Обмотка'])),
            branch__in=branches)
        self.fields['receiving'].queryset = Profile.objects.filter(user__in=User.objects.filter(
            groups__in=Group.objects.filter(name__in=['Ответственные'])),
            branch__in=branches).order_by('user__last_name')
        #self.fields['group_receiving'].queryset = Group.objects.filter(name__in=['ОТК', 'ИТР'])

    name = forms.CharField(label='Наименование работ', required=True)
    complete = forms.BooleanField(label='', required=False)
    date_due = forms.DateField(required=False, label=u'Срок выполнения',
                               widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                               input_formats=('%Y-%m-%d',))
    date_complete = forms.DateField(required=False, label=u'Дата выполнения',
                                    widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                    input_formats=('%Y-%m-%d',))
    date_result = forms.DateField(required=False, label=u'Дата результата',
                                  widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                  input_formats=('%Y-%m-%d',))
    executor = forms.ModelMultipleChoiceField(required=False, label='Исполнитель', queryset=Profile.objects.all(),
                                              widget=forms.SelectMultiple(attrs={'multiple': 'multiple',
                                                                                 'class': 'multi_select'}))

    class Meta:
        model = Completing
        exclude = ()


CompletingFormSet = modelformset_factory(Completing, form=CompletingForm,
                                         fields=['name', 'date_due', 'executor', 'receiving', 'comment'],
                                         extra=1, can_delete=True)


class AssemblyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssemblyForm, self).__init__(*args, **kwargs)
        branches = Profile.objects.get(user=get_current_user()).branch.all()
        self.fields['executor'].queryset = Profile.objects.filter(
            user__in=User.objects.filter(groups__in=Group.objects.filter(name__in=['КИС', 'Обмотка'])),
            branch__in=branches)
        self.fields['receiving'].queryset = Profile.objects.filter(user__in=User.objects.filter(
            groups__in=Group.objects.filter(name__in=['Ответственные'])),
            branch__in=branches)
        #self.fields['group_receiving'].queryset = Group.objects.filter(name__in=['ОТК', 'ИТР'])

    name = forms.CharField(label='Наименование работ', required=True)
    date_due = forms.DateField(required=False, label=u'Срок выполнения',
                               widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                               input_formats=('%Y-%m-%d',))
    executor = forms.ModelMultipleChoiceField(required=False, label='Исполнитель', queryset=Profile.objects.all(),
                                              widget=forms.SelectMultiple(attrs={'multiple': 'multiple',
                                                                                 'class': 'multi_select'}))

    class Meta:
        model = Assembly
        exclude = ()


AssemblyFormSet = modelformset_factory(Assembly, form=AssemblyForm,
                                       fields=['name', 'date_due', 'executor', 'receiving', 'comment'],
                                       extra=1, can_delete=True)


class InvestmentsForm(forms.ModelForm):

    key = forms.CharField(label='Наименование работ', required=True)
    datetime_add = forms.DateField(required=False, label=u'Дата',
                                   widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                   input_formats=('%Y-%m-%d',))

    class Meta:
        model = Investments
        exclude = ()


InvestmentsFormSet = modelformset_factory(Investments, form=InvestmentsForm,
                                          fields=['key', 'file', 'comment'], extra=1, can_delete=False)


# --------------------------------------------------------------------------------------------
# ------------------------------ Делегирование задачи ----------------------------------------
# --------------------------------------------------------------------------------------------
class AssignPerformerForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(AssignPerformerForm, self).__init__(*args, **kwargs)
        branches = Profile.objects.get(user=get_current_user()).branch.all()
        self.fields['executor'].queryset = Profile.objects.filter(
            user__in=User.objects.filter(groups__in=Group.objects.filter(name__in=['КИС', 'Обмотка'])),
            branch__in=branches)

    executor = forms.ModelChoiceField(required=False, label='Исполнитель', widget=forms.Select(), queryset=Profile.objects.all())


# --------------------------------------------------------------------------------------------
# ------------------------------ Контроль выполнения -----------------------------------------
# --------------------------------------------------------------------------------------------
class ForCheckingDisassemblyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ForCheckingDisassemblyForm, self).__init__(*args, **kwargs)

        self.fields['executor'].required = False
        self.fields['executor'].widget.attrs['disabled'] = 'disabled'
        self.fields['name'].required = False
        self.fields['name'].widget.attrs['disabled'] = 'disabled'
        self.fields['date_complete'].required = False
        self.fields['date_complete'].widget.attrs['disabled'] = 'disabled'
        self.fields['comment'].widget = forms.Textarea()

    photo = forms.ImageField(label=u'Фотография контрольная')

    class Meta:
        model = Disassembly
        fields = ['executor', 'name', 'date_complete', 'accepted', 'comment']


class ForCheckingFaultDetectionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ForCheckingFaultDetectionForm, self).__init__(*args, **kwargs)

        self.fields['executor'].required = False
        self.fields['executor'].widget.attrs['disabled'] = 'disabled'
        self.fields['name'].required = False
        self.fields['name'].widget.attrs['disabled'] = 'disabled'
        self.fields['date_complete'].required = False
        self.fields['date_complete'].widget.attrs['disabled'] = 'disabled'

    photo = forms.ImageField(label=u'Фотография контрольная')

    class Meta:
        model = FaultDetection
        fields = ['executor', 'name', 'type_work', 'count_components', 'count_order',
                  'date_complete', 'result']


class ForCheckingMechanicsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ForCheckingMechanicsForm, self).__init__(*args, **kwargs)

        self.fields['executor'].required = False
        self.fields['executor'].widget.attrs['disabled'] = 'disabled'
        self.fields['name'].required = False
        self.fields['name'].widget.attrs['disabled'] = 'disabled'
        self.fields['date_complete'].required = False
        self.fields['date_complete'].widget.attrs['disabled'] = 'disabled'
        self.fields['comment'].widget = forms.Textarea()

    photo = forms.ImageField(label=u'Фотография контрольная')

    class Meta:
        model = Mechanics
        fields = ['executor', 'name', 'price', 'degrees_0', 'degrees_120', 'degrees_240', 'material',
                  'date_complete', 'comment', 'result']


class ForCheckingTestsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ForCheckingTestsForm, self).__init__(*args, **kwargs)

        self.fields['executor'].required = False
        self.fields['executor'].widget.attrs['disabled'] = 'disabled'

    photo = forms.ImageField(label=u'Фотография контрольная')

    class Meta:
        model = Tests
        fields = ['executor', 'indications', 'stator', 'rotor_cage']


class ForCheckingPolesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ForCheckingPolesForm, self).__init__(*args, **kwargs)

        self.fields['executor'].required = False
        self.fields['executor'].widget.attrs['disabled'] = 'disabled'
        self.fields['name'].required = False
        self.fields['name'].widget.attrs['disabled'] = 'disabled'
        self.fields['date_complete'].required = False
        self.fields['date_complete'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = Poles
        fields = ['executor', 'name', 'date_complete', 'result', 'comment']


class ForCheckingSectionsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ForCheckingSectionsForm, self).__init__(*args, **kwargs)

        self.fields['executor'].required = False
        self.fields['executor'].widget.attrs['disabled'] = 'disabled'
        self.fields['name'].required = False
        self.fields['name'].widget.attrs['disabled'] = 'disabled'
        self.fields['date_complete'].required = False
        self.fields['date_complete'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = Sections
        fields = ['executor', 'name', 'date_complete', 'result', 'comment']


class ForCheckingInductorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ForCheckingInductorForm, self).__init__(*args, **kwargs)

        self.fields['executor'].required = False
        self.fields['executor'].widget.attrs['disabled'] = 'disabled'
        self.fields['name'].required = False
        self.fields['name'].widget.attrs['disabled'] = 'disabled'
        self.fields['date_complete'].required = False
        self.fields['date_complete'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = Inductor
        fields = ['executor', 'name', 'date_complete', 'result', 'comment']


class ForCheckingAnchorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ForCheckingAnchorForm, self).__init__(*args, **kwargs)

        self.fields['executor'].required = False
        self.fields['executor'].widget.attrs['disabled'] = 'disabled'
        self.fields['name'].required = False
        self.fields['name'].widget.attrs['disabled'] = 'disabled'
        self.fields['date_complete'].required = False
        self.fields['date_complete'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = Anchor
        fields = ['executor', 'name', 'date_complete', 'result', 'comment']


class ForCheckingShieldsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ForCheckingShieldsForm, self).__init__(*args, **kwargs)

        self.fields['executor'].required = False
        self.fields['executor'].widget.attrs['disabled'] = 'disabled'
        self.fields['name'].required = False
        self.fields['name'].widget.attrs['disabled'] = 'disabled'
        self.fields['date_complete'].required = False
        self.fields['date_complete'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = Shields
        fields = ['executor', 'name', 'date_complete', 'result', 'comment']


class ForCheckingSpindleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ForCheckingSpindleForm, self).__init__(*args, **kwargs)

        self.fields['executor'].required = False
        self.fields['executor'].widget.attrs['disabled'] = 'disabled'
        self.fields['name'].required = False
        self.fields['name'].widget.attrs['disabled'] = 'disabled'
        self.fields['date_complete'].required = False
        self.fields['date_complete'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = Spindle
        fields = ['executor', 'name', 'date_complete', 'result', 'comment']


class ForCheckingCompletingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ForCheckingCompletingForm, self).__init__(*args, **kwargs)

        self.fields['executor'].required = False
        self.fields['executor'].widget.attrs['disabled'] = 'disabled'
        self.fields['name'].required = False
        self.fields['name'].widget.attrs['disabled'] = 'disabled'
        self.fields['date_complete'].required = False
        self.fields['date_complete'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = Completing
        fields = ['executor', 'name', 'date_complete', 'result', 'comment']


class ForCheckingAssemblyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ForCheckingAssemblyForm, self).__init__(*args, **kwargs)

        self.fields['executor'].required = False
        self.fields['executor'].widget.attrs['disabled'] = 'disabled'
        self.fields['name'].required = False
        self.fields['name'].widget.attrs['disabled'] = 'disabled'
        self.fields['date_complete'].required = False
        self.fields['date_complete'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = Assembly
        fields = ['executor', 'name', 'date_complete', 'result', 'comment']
