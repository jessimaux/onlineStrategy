from django import forms
from django.forms import modelformset_factory, BaseModelFormSet, inlineformset_factory, BaseInlineFormSet
from .models import Answer, Question, Municipality, MethodMunicipality, Diagnostic
from accounts.models import Account


class BaseQuestionAnswerFormset(BaseModelFormSet):
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

QFormSet = modelformset_factory(Question, AnswerForm, formset=BaseQuestionAnswerFormset, extra=0)


class OrderingForm(forms.Form):
    ordering = forms.CharField()


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


class DiagnosticCreateForm(forms.ModelForm):
    q_count = forms.IntegerField()
    class Meta:
        model = Diagnostic
        fields =['title', 'description']


class DiagnosticUpdateForm(forms.ModelForm):
    class Meta:
        model = Diagnostic
        fields = ['title', 'description']


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'mark1', 'mark2', 'mark3', 'mark4']


class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['ans', 'correct']


AnswerCreateInlineFormset = inlineformset_factory(Question, Answer, form=AnswerCreateForm, can_delete=True, extra=0)