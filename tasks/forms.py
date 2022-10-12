from datetime import datetime, timedelta
from django import forms

from tasks.models import Tasks


class TasksArchiveForm(forms.Form):
    start_period = forms.DateField(required=False, label=u'Начало периода',
                                   widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                   input_formats=('%Y-%m-%d',), initial=datetime.today().replace(day=1))
    end_period = forms.DateField(required=False, label=u'Конец периода', initial=datetime.date(datetime.today()),
                                 widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                 input_formats=('%Y-%m-%d',))


class KanbanForm(forms.Form):
    curr_week = forms.DateField(required=False, label=u'Неделя', initial=datetime.today().strftime("%V"),
                                widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'week'}),
                                input_formats=('%Y-%m-%d',))
    curr_day = forms.DateField(required=False, label=u'День', initial=datetime.today()+timedelta(days=1),
                               widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                               input_formats=('%Y-%m-%d',))
