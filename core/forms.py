from django import forms
from django.forms import modelformset_factory, BaseModelFormSet, inlineformset_factory, BaseInlineFormSet
from .models import Answer, Question, Municipality, MethodMunicipality, Diagnostic
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


AnswerCreateFormset = inlineformset_factory(Question, Answer, fields=['ans', 'correct'], extra=1)


class BaseQuestionCreateFormset(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(BaseQuestionCreateFormset, self).add_fields(form, index)

        form.nested = AnswerCreateFormset(
                        instance=form.instance,
                        data=form.data if form.is_bound else None,
                        files=form.files if form.is_bound else None,
                        prefix='answer-%s-%s' % (
                            form.prefix,
                            AnswerCreateFormset.get_default_prefix()))


QuestionCreateFormset = inlineformset_factory(Diagnostic,
                                              Question,
                                              formset=BaseQuestionCreateFormset,
                                              fields=['title', 'mark1'],
                                              extra=0)
