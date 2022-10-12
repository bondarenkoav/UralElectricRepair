from django import forms

from repairshop.models import Disassembly, FaultDetection, Mechanics, Tests, \
    Poles, Sections, Inductor, Anchor, Shields, Spindle, Completing, Assembly


class ArchiveForm(forms.Form):
    start_period = forms.DateField(required=False, label=u'Начало периода',
                                   widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                   input_formats=('%Y-%m-%d',))#, initial=datetime.today().replace(day=1))
    end_period = forms.DateField(required=False, label=u'Конец периода', #initial=datetime.date(datetime.today()),
                                 widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
                                 input_formats=('%Y-%m-%d',))


class ToPerformDisassemblyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ToPerformDisassemblyForm, self).__init__(*args, **kwargs)

        self.fields['name'].required = False
        self.fields['name'].widget.attrs['disabled'] = 'disabled'
        self.fields['date_due'].required = False
        self.fields['date_due'].widget.attrs['disabled'] = 'disabled'
        self.fields['comment'].widget = forms.Textarea()

    photo = forms.ImageField(label=u'Фотография выполненой работы')

    class Meta:
        model = Disassembly
        fields = ['complete', 'comment']


class ToPerformFaultDetectionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ToPerformFaultDetectionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FaultDetection
        fields = ['general_info', 'type_work', 'count_components', 'count_order', 'complete']


class ToPerformMechanicsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ToPerformMechanicsForm, self).__init__(*args, **kwargs)

        self.fields['comment'].widget = forms.Textarea()

    photo = forms.ImageField(label=u'Фото')

    class Meta:
        model = Mechanics
        fields = ['degrees_0', 'degrees_120', 'degrees_240', 'seat_diameter', 'material', 'comment', 'complete']


class ToPerformTestsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ToPerformTestsForm, self).__init__(*args, **kwargs)

    photo = forms.ImageField(label=u'Фото')

    class Meta:
        model = Tests
        fields = ['stator', 'rotor_cage', 'rings', 'complete']


class ToPerformPolesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ToPerformPolesForm, self).__init__(*args, **kwargs)

        self.fields['comment'].widget = forms.Textarea()

    class Meta:
        model = Poles
        fields = ['name', 'date_due', 'complete', 'comment']


class ToPerformSectionsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ToPerformSectionsForm, self).__init__(*args, **kwargs)

        self.fields['comment'].widget = forms.Textarea()

    class Meta:
        model = Sections
        fields = ['complete', 'comment']


class ToPerformInductorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ToPerformInductorForm, self).__init__(*args, **kwargs)

        self.fields['comment'].widget = forms.Textarea()

    class Meta:
        model = Inductor
        fields = ['complete', 'comment']


class ToPerformAnchorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ToPerformAnchorForm, self).__init__(*args, **kwargs)

        self.fields['comment'].widget = forms.Textarea()

    class Meta:
        model = Anchor
        fields = ['complete', 'comment']


class ToPerformShieldsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ToPerformShieldsForm, self).__init__(*args, **kwargs)

        self.fields['comment'].widget = forms.Textarea()

    class Meta:
        model = Shields
        fields = ['complete', 'comment']


class ToPerformSpindleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ToPerformSpindleForm, self).__init__(*args, **kwargs)

        self.fields['comment'].widget = forms.Textarea()

    class Meta:
        model = Spindle
        fields = ['complete', 'comment']


class ToPerformCompletingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ToPerformCompletingForm, self).__init__(*args, **kwargs)

        self.fields['comment'].widget = forms.Textarea()

    class Meta:
        model = Completing
        fields = ['complete', 'comment']


class ToPerformAssemblyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ToPerformAssemblyForm, self).__init__(*args, **kwargs)

        self.fields['comment'].widget = forms.Textarea()

    class Meta:
        model = Assembly
        fields = ['complete', 'comment']
