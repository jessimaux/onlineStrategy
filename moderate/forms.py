from django import forms
from django.forms import inlineformset_factory
from method.models import MethodMunicipality
from core.models import Municipality
from accounts.models import Account


class MethodMunicipalityForm(forms.ModelForm):
    method = forms.ModelChoiceField(queryset=Account.objects.filter(methodist=True))

    class Meta:
        model = MethodMunicipality
        fields = ['method']

MethodMunicipalityInlineFormset = inlineformset_factory(Municipality,
                                                        MethodMunicipality,
                                                        form=MethodMunicipalityForm,
                                                        can_delete=True,
                                                        extra=1)