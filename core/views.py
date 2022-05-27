from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from onlineStrategy.permissions import ModeratorPermissionsMixin

from django.views.generic import ListView, TemplateView, FormView
from django.http import HttpResponseRedirect

from courses.models import Course, AccountCourse
from accounts.models import Account
from .models import Question, Answer, Diagnostic, DiagnosticResult

from django.db.models import Q

from .forms import QuestionFormSet, AnswerForm


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'core/index.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return AccountCourse.objects.filter(account_id=self.request.user.id)
        #return Course.objects.filter(accountcourse__account_id=self.request.user.id)


class RouteProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'core/route-profile.html'


class DiagnosticListView(LoginRequiredMixin, ListView):
    template_name = 'core/route-diagnostics.html'
    context_object_name = 'object_list'
    model = Diagnostic


class DiagnosticDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'core/route-diagnostics-item.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data()
        object_list = Question.objects.filter(diagnostic=self.kwargs['pk'])
        qs = list(object_list)
        context['formset'] = QuestionFormSet(queryset=object_list, form_kwargs={'question_id': qs})
        return context

    def post(self, request, *args, **kwargs):
        object_list = Question.objects.filter(diagnostic=self.kwargs['pk'])
        qs = list(object_list)
        formset = QuestionFormSet(request.POST, form_kwargs={'question_id': qs})
        if formset.is_valid():
            return self.form_valid(formset)

    def form_valid(self, formset):
        mark = 0
        for form in formset:
            form_obj = form.save(commit=False)
            if form_obj.correct:
                mark += 1
        DiagnosticResult.objects.get_or_create(diagnostic=Diagnostic(id=self.kwargs['pk']),
                                               account=Account(id=self.request.user.pk),
                                               mark=mark)
        return HttpResponseRedirect('/courses')

    def get(self, request, *args, **kwargs):
        try:
            obj = DiagnosticResult.objects.get(account_id=self.request.user.pk,
                                               diagnostic_id=self.kwargs['pk'])
        except DiagnosticResult.DoesNotExist:
            obj = None
        if obj:
            return redirect('route-profile')
        else:
            return super(DiagnosticDetailView, self).get(request, *args, **kwargs)


# old version wo using form
'''
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['questions'] = Question.objects.filter(diagnostic_id=self.kwargs['pk'])
        return context

    def post(self, request, *arg, **kwargs):
        for key, value in request.POST.dict().items():
            if key.startswith('flexRadio-') and Answer.objects.get(id=value).correct == 1:
                print('ok')
        return self.get(request, *arg, **kwargs)
'''


class ModerateProfilesListView(LoginRequiredMixin, ModeratorPermissionsMixin, ListView):
    template_name = 'core/moderate-profiles.html'
    context_object_name = 'object_list'
    model = Account
    paginate_by = 50

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(Q(first_name__icontains=query) |
                                                    Q(last_name__icontains=query) |
                                                    Q(middle_name__icontains=query) |
                                                    Q(subject_of_country__icontains=query) |
                                                    Q(municipality__icontains=query) |
                                                    Q(work__icontains=query)
                                                    )
            return object_list
        else:
            return super(ModerateProfilesListView, self).get_queryset()


class ModerateCoursesListView(LoginRequiredMixin, ModeratorPermissionsMixin, ListView):
    template_name = 'core/moderate-courses.html'
    context_object_name = 'object_list'
    model = Course
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(title__icontains=query)
            return object_list
        else:
            return super(ModerateCoursesListView, self).get_queryset()


class ModerateAccountView(LoginRequiredMixin, ModeratorPermissionsMixin, TemplateView):
    template_name = 'core/moderate-profile-card.html'

    def get_context_data(self, **kwargs):
        context = super(ModerateAccountView, self).get_context_data()
        context['profile'] = Account.objects.filter(id=self.kwargs['pk']).values('first_name',
                                                                                 'last_name',
                                                                                 'middle_name',
                                                                                 'email',
                                                                                 'date_of_birth',
                                                                                 'work',
                                                                                 'municipality',
                                                                                 'phone_number',
                                                                                 'subject_of_country')[0]
        context['signs'] = AccountCourse.objects.filter(account_id=self.kwargs['pk'])
        return context