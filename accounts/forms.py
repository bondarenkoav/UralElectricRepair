from django import forms

from accounts.models import Profile

__author__ = 'ipman'


# Форма добавления поставки
class FormLoadAvatar(forms.ModelForm):
    avatar = forms.ImageField(label=u'Выберите изображение')

    class Meta:
        model = Profile
        fields = ['avatar']
