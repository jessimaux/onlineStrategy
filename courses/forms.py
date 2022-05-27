from django import forms
from .models import Course, CourseProgram
from .models import AccountCourse, STATUS_CHOICES
from django.forms import modelformset_factory, Form, ChoiceField, CharField


class AccountCourseInListForm(forms.ModelForm):
    status = forms.ChoiceField(choices=STATUS_CHOICES,
                               widget=forms.Select(attrs={'onchange': 'submit();'}))

    class Meta:
        model = AccountCourse
        fields = ['status']


SignFormSet = modelformset_factory(AccountCourse, AccountCourseInListForm, extra=0)


class ProgramForm(forms.ModelForm):
    class Meta:
        model = CourseProgram
        fields = ['item', 'duration']


ProgramFormSet = modelformset_factory(CourseProgram, ProgramForm, extra=0)


class FilterForm(Form):
    PROFILE_CHOICES = (
        ('', 'Все профили'),
        ('Предметные', 'Предметные'),
        ('Метапредметные', 'Метапредметные'),
        ('Управленческие', 'Управленческие'),
    )

    SUBJECT_CHOICES = (
        ('', 'Все предметы'),
        ('Биология', 'Биология'),
        ('Математика', 'Математика'),
    )
    search = CharField(required=False)
    profile = ChoiceField(choices=PROFILE_CHOICES, required=False)
    subject = ChoiceField(choices=SUBJECT_CHOICES, required=False)