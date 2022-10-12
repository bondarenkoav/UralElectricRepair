from django.forms import ModelForm, forms, modelformset_factory
from reference_books.models import Client, Posts, ModelEquipment


class ClientForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.user = kwargs.pop('user', None)

        self.fields['type'].required = True

    class Meta:
        model = Client
        fields = ['type', 'name', 'inn', 'kpp']


class PostForm(ModelForm):
    class Meta:
        model = Posts
        fields = ['name', 'slug']


class EquipmentForm(ModelForm):
    class Meta:
        model = ModelEquipment
        fields = ['type', 'amperage', 'name', 'p', 'u', 'n', 'unn', 'uvn']