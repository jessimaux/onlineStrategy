from django import forms


class OrderingForm(forms.Form):
    ordering = forms.CharField()