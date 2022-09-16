from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordResetForm
from .models import Account

from core.models import Municipality


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(max_length=32)
    last_name = forms.CharField(max_length=32)
    middle_name = forms.CharField(max_length=32, required=False)
    date_of_birth = forms.DateField()
    f_agree = forms.BooleanField()

    class Meta:
        model = Account
        fields = ('email', 'first_name', 'last_name', 'middle_name', 'date_of_birth')


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'image', 'first_name', 'last_name', 'middle_name', 'gender', 'date_of_birth', 'national',
                  'phone_number', 'municipality', 'education_level', 'education_document_serial',
                  'education_document_number',  'education_document_reg_number', 'education_document_date',
                  'education_document_second_name', 'education_document_first_name', 'education_document_middle_name',
                  'education_qualify', 'education_pow', 'education_rank', 'work', 'work_pos', 'work_exp', 'work_edu_exp', 'document_serial',
                  'document_number',  'document_department',  'document_date', 'document_code_department',
                  'document_place_birth']


class AccountPasswordResetForm(PasswordResetForm):
    def clean(self):
        cleaned_data = super().clean()
        try:
            email = Account.objects.get(email=cleaned_data.get('email'))
        except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
            email = None
        if email is None:
            raise forms.ValidationError(
                'Пользователь с такими данными не найден или автоматическая смена пароля невозможна!'
            )