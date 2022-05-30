from django import forms
from django.forms import modelformset_factory, BaseModelFormSet
from .models import Answer, Question
from accounts.models import Account


class BaseQuestionFormSet(BaseModelFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        q = kwargs['question_id'][index]
        # note that instead of passing a dictionary which includes a copy
        # of the formset's `form_kwargs`, we actually return a dictionary
        # that holds a single key-value pair
        return {'question_id': q}


class AnswerForm(forms.ModelForm):
    answers = forms.ModelChoiceField(label=False, widget=forms.RadioSelect, queryset=Answer.objects.all())
    title = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Answer
        fields = ['title']

    def __init__(self, question_id, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)

        if question_id:
            self.fields['answers'].queryset = Answer.objects.filter(question_id=question_id)

QuestionFormSet = modelformset_factory(Question, AnswerForm, formset=BaseQuestionFormSet, extra=0)


class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Account
        fields = ('image',)