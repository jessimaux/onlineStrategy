from django.contrib.auth.mixins import LoginRequiredMixin
from onlineStrategy.permissions import ModeratorPermissionsMixin

from django.views.generic import ListView, TemplateView, CreateView, DeleteView
from django.http import HttpResponseRedirect

from accounts.models import Account
from .models import Question, Diagnostic, DiagnosticResult

from .forms import QFormSet, DiagnosticCreateForm, QuestionCreateForm, AnswerCreateInlineFormset, DiagnosticUpdateForm

from django.urls import reverse_lazy


class DiagnosticDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'route/route-diagnostics-item.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        object_list = Question.objects.filter(diagnostic=self.kwargs['pk'])
        qs = list(object_list)
        context['formset'] = QFormSet(queryset=object_list, form_kwargs={'question_id': qs})
        context['diagnostic'] = Diagnostic.objects.get(id=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        object_list = Question.objects.filter(diagnostic=self.kwargs['pk'])
        qs = list(object_list)
        formset = QFormSet(request.POST, form_kwargs={'question_id': qs})
        if formset.is_valid():
            return self.form_valid(formset)

    def form_valid(self, formset):
        mark1, mark2, mark3, mark4 = 0, 0, 0, 0
        for form in formset:
            form_obj = form.save(commit=False)
            if form.is_valid():
                if form.cleaned_data['answers'].correct:
                    if form_obj.mark1:
                        mark1 += 1
                    if form_obj.mark2:
                        mark2 += 1
                    if form_obj.mark3:
                        mark3 += 1
                    if form_obj.mark4:
                        mark4 += 1
        DiagnosticResult.objects.get_or_create(diagnostic=Diagnostic(id=self.kwargs['pk']),
                                               account=Account(id=self.request.user.pk),
                                               mark1=mark1,
                                               mark2=mark2,
                                               mark3=mark3,
                                               mark4=mark4)
        return HttpResponseRedirect(reverse_lazy('index'))

    def get(self, request, *args, **kwargs):
        try:
            obj = DiagnosticResult.objects.get(account_id=self.request.user.pk,
                                               diagnostic_id=self.kwargs['pk'])
        except DiagnosticResult.DoesNotExist:
            obj = None
        if obj:
            return HttpResponseRedirect(reverse_lazy('route-diagnostics-result', args=[self.kwargs['pk']]))
            #return redirect('route-diagnostics-result')
        else:
            return super(DiagnosticDetailView, self).get(request, *args, **kwargs)


class DiagnosticsCreateView(LoginRequiredMixin, ModeratorPermissionsMixin, CreateView):
    template_name = 'diagnostics/diagnostics-create.html'
    success_url = reverse_lazy('moderate-diagnostics')
    form_class = DiagnosticCreateForm

    def form_valid(self, form):
        response = super(DiagnosticsCreateView, self).form_valid(form)
        for i in range(form.cleaned_data["q_count"]):
            Question.objects.create(diagnostic_id=form.instance.pk)
        return response


class DiagnosticsUpdateView(LoginRequiredMixin, ModeratorPermissionsMixin, TemplateView):
    template_name = 'diagnostics/diagnostics-update.html'

    def get_context_data(self, **kwargs):
        context = super(DiagnosticsUpdateView, self).get_context_data()

        q_query = Question.objects.filter(diagnostic_id=self.kwargs['pk'])
        temp_q = list()
        temp_a = list()

        for i in range(len(q_query)):
            temp_q.append(QuestionCreateForm(instance=q_query[i], prefix='q_form-' + str(i)))
            temp_a.append(AnswerCreateInlineFormset(instance=q_query[i], prefix='a_formset-' + str(i)))

        context['formsets'] = zip(temp_q, temp_a)
        context['diagnostic_form'] = DiagnosticUpdateForm(instance=Diagnostic.objects.get(id=self.kwargs['pk']))
        return context

    def post(self, *args, **kwargs):
        q_query = Question.objects.filter(diagnostic_id=self.kwargs['pk'])

        diagnostic_form = DiagnosticUpdateForm(data=self.request.POST,
                                               instance=Diagnostic.objects.get(id=self.kwargs['pk']))
        temp_q = list()
        temp_a = list()

        for i in range(len(q_query)):
            temp_q.append(QuestionCreateForm(self.request.POST, instance=q_query[i], prefix='q_form-' + str(i)))
            temp_a.append(AnswerCreateInlineFormset(data=self.request.POST,
                                                    instance=q_query[i],
                                                    prefix='a_formset-' + str(i)))

        formsets = zip(temp_q, temp_a)

        if diagnostic_form.is_valid():
            diagnostic_form.save()

        for q_form, formset in formsets:
            if q_form.is_valid() and formset.is_valid():
                q_form.save()
                formset.save(commit=False)

                for form in formset:
                    form_obj = form.save(commit=False)
                    if form_obj.question_id:
                        form_obj.save()

                for obj in formset.deleted_objects:
                    obj.delete()

        return HttpResponseRedirect(reverse_lazy('moderate-diagnostics'))


class DiagnosticsDeleteView(LoginRequiredMixin, ModeratorPermissionsMixin, DeleteView):
    model = Diagnostic
    success_url = reverse_lazy('moderate-diagnostics')


# TODO: Structure - maybe move it to core or route?
# app have only functional view, core for the list and etc
class DiagnosticListView(LoginRequiredMixin, ListView):
    template_name = 'route/route-diagnostics.html'
    context_object_name = 'object_list'
    model = Diagnostic
    paginate_by = 10
    ordering = 'id'


class DiagnosticResultView(LoginRequiredMixin, TemplateView):
    template_name = 'route/route-diagnostics-result.html'

    def get_context_data(self, **kwargs):
        context = super(DiagnosticResultView, self).get_context_data()
        diagnostics_results = DiagnosticResult.objects.get(account_id=self.request.user.id,
                                                           diagnostic_id=self.kwargs['pk'])
        context['result'] = [diagnostics_results.mark1,
                             diagnostics_results.mark2,
                             diagnostics_results.mark3,
                             diagnostics_results.mark4]
        return context

