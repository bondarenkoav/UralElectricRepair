from datetime import datetime
from django import forms
from django.contrib.auth.models import Group, User
from django.forms import CheckboxInput
from django_currentuser.middleware import get_current_user

from accounts.models import Profile
from reference_books.models import Client, StatusTask


class FilterWorksForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(FilterWorksForm, self).__init__(*args, **kwargs)
        branches = Profile.objects.get(user=get_current_user()).branch.all()
        self.fields['executor'].queryset = Profile.objects.filter(
            user__in=User.objects.filter(groups__in=Group.objects.all()), branch__in=branches)
        self.fields['author'].queryset = Profile.objects.filter(
            user__in=User.objects.filter(groups__in=Group.objects.filter(name__in=['ОТК', 'ИТР'])), branch__in=branches)

    startdate = forms.DateField(label=u'Дата', initial=datetime.today, required=False,
                                widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                input_formats=('%Y-%m-%d',))
    enddate = forms.DateField(label=u'Дата', required=False,
                              widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                              input_formats=('%Y-%m-%d',))
    norangedate = forms.BooleanField(label=u'За весь период', required=False, widget=CheckboxInput)
    executor = forms.ModelChoiceField(label=u'Исполнитель', required=False, queryset=Profile.objects.all(),
                                      widget=forms.Select(attrs={'class': 'selector'}))
    author = forms.ModelChoiceField(label=u'Ответственный', required=False, queryset=Profile.objects.filter(),
                                    widget=forms.Select(attrs={'class': 'selector'}))
    client = forms.ModelChoiceField(label=u'Контрагент', required=False, queryset=Client.objects.all(),
                                    widget=forms.Select(attrs={'class': 'selector'}))
    status = forms.ModelChoiceField(label=u'Состояние', required=False, queryset=StatusTask.objects.all(),
                                    widget=forms.Select(attrs={'class': 'selector'}))

    def clean(self):
        cleaned_data = super(FilterWorksForm, self).clean()
        startdate = cleaned_data['startdate']
        enddate = cleaned_data['enddate']

        if startdate is None:
            self._errors['startdate'] = self.error_class([u'Введите дату поиска'])
        if enddate is not None and enddate < startdate:
            self._errors['enddate'] = self.error_class([u'Дата окончания периода должна быть позже даты начала'])

        return cleaned_data
