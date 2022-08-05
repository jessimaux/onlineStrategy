from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.mixins import LoginRequiredMixin
from onlineStrategy.permissions import ModeratorPermissionsMixin, MethodistPermissionsMixin

from django.views.generic import ListView, TemplateView, UpdateView, CreateView, DeleteView, FormView
from django.http import HttpResponseRedirect

from courses.models import Course, AccountCourse
from accounts.models import Account
from .models import Question, Diagnostic, DiagnosticResult, Methodist2Teacher, MethodistLessonSigns, RouteManual, Route,\
    Events, MethodMunicipality, Municipality

from django.db.models import Q

from .forms import QuestionFormSet, OrderingForm, MethodMunicipalityInlineFormset

from django.urls import reverse_lazy
from django.contrib import messages
from .tools import negative_number_is_zero

from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.shortcuts import render

from datetime import date


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data()

        # Notify manager need rework
        """
        lesson_sign_list = MethodistLessonSigns.objects.filter(teacher_id=self.request.user.id)
        acc_course_list = AccountCourse.objects.filter(account_id=self.request.user.id)

        course_list = list()
        for course in acc_course_list:
            if course.course_id not in course_list:
                course_list.append(course.course_id)

        context['notify_list'] = Events.objects.filter(Q(object_id__in=acc_course_list.values('id'),
                                                         content_type__pk=ContentType.objects.get_for_model(AccountCourse).id) |
                                                       Q(object_id__in=course_list,
                                                         content_type__pk=ContentType.objects.get_for_model(Course).id) |
                                                       Q(object_id__in=lesson_sign_list.values('id'),
                                                         content_type__pk=ContentType.objects.get_for_model(MethodistLessonSigns).id)).order_by('date').reverse()[:15]

        context['type_dict'] = {'AccCourse': ContentType.objects.get_for_model(AccountCourse).id,
                                'Course': ContentType.objects.get_for_model(Course).id,
                                'LessonSign': ContentType.objects.get_for_model(MethodistLessonSigns).id}
        """

        total_mark1, total_mark2, total_mark3, total_mark4 = 0, 0, 0, 0
        diagnostics_results = DiagnosticResult.objects.filter(account_id=self.request.user.id)
        for res in diagnostics_results:
            total_mark1 += res.mark1
            total_mark2 += res.mark2
            total_mark3 += res.mark3
            total_mark4 += res.mark4

        context['result_exists'] = diagnostics_results.exists()
        context['result'] = [total_mark1, total_mark2, total_mark3, total_mark4]
        context['account'] = Account.objects.get(id=self.request.user.id)

        try:
            context['active_lesson'] = MethodistLessonSigns.objects.get(teacher_id=self.request.user.id,
                                                                        status__in=('СМОТР', 'ОДОБР'))
        except MethodistLessonSigns.DoesNotExist:
            context['active_lesson'] = None

        try:
            context['method'] = Methodist2Teacher.objects.get(teacher_id=self.request.user.id)
        except Methodist2Teacher.DoesNotExist:
            context['method'] = None

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        lesson_signs = MethodistLessonSigns.objects.filter(teacher_id=self.request.user.id)
        paginator_lesson_signs = Paginator(lesson_signs, 10)
        page_number_lesson_signs = self.request.GET.get('lpage')
        lpage_obj = paginator_lesson_signs.get_page(page_number_lesson_signs)
        context['lpage_obj'] = lpage_obj

        course_signs = AccountCourse.objects.filter(account_id=self.request.user.id)
        paginator_course_signs = Paginator(course_signs, 10)
        page_number_course_signs = self.request.GET.get('cpage')
        cpage_obj = paginator_course_signs.get_page(page_number_course_signs)
        context['cpage_obj'] = cpage_obj

        return self.render_to_response(context)


class RouteManualsListView(LoginRequiredMixin, ListView):
    template_name = 'core/route-manuals.html'
    context_object_name = 'object_list'
    model = RouteManual
    paginate_by = 25

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(Q(title__icontains=query) |
                                                    Q(author__icontains=query))
            return object_list
        else:
            return super().get_queryset()


def add2route_manual(request, *args, **kwargs):
    if request.user.is_authenticated:
        try:
            obj = Route.objects.get(account=Account(id=request.user.pk),
                                    manual=RouteManual(id=kwargs['pk']))
            messages.success(request, 'Материал уже находится в вашем образовательном маршруте')
        except Route.DoesNotExist:
            Route(account=Account(id=request.user.pk),
                  manual=RouteManual(id=kwargs['pk'])).save()
            messages.success(request, 'Материал добавлен в ваш образовательный маршрут')
        return HttpResponseRedirect('/route')


class RouteView(LoginRequiredMixin, TemplateView):
    template_name = 'core/route.html'
    
    def get_context_data(self, **kwargs):
        context = super(RouteView, self).get_context_data()
        context['route'] = Route.objects.filter(account_id=self.request.user.id).order_by('order')

        """ selection manuals """
        # TODO: random queryset w max pos 50
        try:
            profile = DiagnosticResult.objects.get(account_id=self.request.user.id)
            context['diagnostics_exists'] = True
        except DiagnosticResult.DoesNotExist:
            context['diagnostics_exists'] = False
            return context

        using_manuals = Route.objects.filter(account_id=self.request.user.id)
        manuals = RouteManual.objects.exclude(id__in=using_manuals.values('manual_id'))
        context['recommendation'] = list()

        for manual in manuals:
            dist = (negative_number_is_zero(manual.mark1 - profile.mark1)**2 +
                    negative_number_is_zero(manual.mark2 - profile.mark2)**2 +
                    negative_number_is_zero(manual.mark3 - profile.mark3)**2 +
                    negative_number_is_zero(manual.mark4 - profile.mark4) ** 2) ** (1/2)
            if dist >= 5:
                context['recommendation'].append(manual)

        return context

    def post(self, request, *args, **kwargs):
        form = OrderingForm(request.POST)
        if form.is_valid():
            ordered_ids = form.cleaned_data["ordering"].split('&')
            c_order = 1
            for id in ordered_ids:
                manual = Route.objects.get(account_id=self.request.user.id, manual_id=id)
                manual.order = c_order
                manual.save()
                c_order += 1
        return HttpResponseRedirect('/route')


class RouteDeleteView(LoginRequiredMixin, DeleteView):
    model = Route
    success_url = reverse_lazy('route')


class RouteUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'core/route-item.html'
    model = Route
    fields = ['deadline', 'status', 'reflection']
    success_url = '/route'


class RouteSignsCreateView(LoginRequiredMixin, CreateView):
    model = MethodistLessonSigns
    fields = ['lesson_title', 'lesson_description', 'lesson_plan', 'date', 'meet_type', 'meet_link']
    template_name = 'core/route-signs-up.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.teacher_id = self.request.user.id
        form.save()
        return super().form_valid(form)


class RouteSignsUpdateView(LoginRequiredMixin, UpdateView):
    model = MethodistLessonSigns
    fields = ['lesson_title', 'lesson_description', 'lesson_plan', 'date', 'meet_type', 'meet_link', 'methodist_comment']
    template_name = 'core/route-signs-update.html'
    success_url = reverse_lazy('route-profile')


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
        return HttpResponseRedirect('/route/profile')

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


class DiagnosticResultView(LoginRequiredMixin, TemplateView):
    template_name = 'core/route-diagnostics-result.html'

    def get_context_data(self, **kwargs):
        context = super(DiagnosticResultView, self).get_context_data()
        diagnostics_results = DiagnosticResult.objects.get(account_id=self.request.user.id,
                                                           diagnostic_id=self.kwargs['pk'])
        context['result'] = [diagnostics_results.mark1,
                             diagnostics_results.mark2,
                             diagnostics_results.mark3,
                             diagnostics_results.mark4]
        return context


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


class ModerateManualsListView(LoginRequiredMixin, ModeratorPermissionsMixin, ListView):
    template_name = 'core/moderate-manuals.html'
    context_object_name = 'object_list'
    model = RouteManual
    paginate_by = 25

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(Q(title__icontains=query) |
                                                    Q(author__icontains=query))
            return object_list
        else:
            return super().get_queryset()


class ModerateManualsCreateView(LoginRequiredMixin, ModeratorPermissionsMixin, CreateView):
    model = RouteManual
    fields = '__all__'
    template_name = 'core/moderate-manuals-create.html'


class ModerateManualsUpdateView(LoginRequiredMixin, ModeratorPermissionsMixin, UpdateView):
    model = RouteManual
    template_name = 'core/moderate-manuals-update.html'
    fields = '__all__'


class ModerateManualsDeleteView(LoginRequiredMixin, ModeratorPermissionsMixin, DeleteView):
    model = RouteManual
    success_url = reverse_lazy('moderate-manuals')


class MethodProfilesListView(LoginRequiredMixin, MethodistPermissionsMixin, ListView):
    template_name = 'core/method-profiles.html'
    context_object_name = 'object_list'
    model = Methodist2Teacher
    paginate_by = 50

    def get_queryset(self):
        object_list = Methodist2Teacher.objects.filter(methodist_id=self.request.user.id)
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(Q(teacher__first_name__icontains=query) |
                                                    Q(teacher__last_name__icontains=query) |
                                                    Q(teacher__middle_name__icontains=query) |
                                                    Q(teacher__subject_of_country__icontains=query) |
                                                    Q(teacher__municipality__icontains=query) |
                                                    Q(teacher__work__icontains=query)
                                                    )
        return object_list


class MethodSignsListView(LoginRequiredMixin, MethodistPermissionsMixin, ListView):
    template_name = 'core/method-signs.html'
    context_object_name = 'object_list'
    model = MethodistLessonSigns
    paginate_by = 25

    def get_queryset(self):
        method_obj = Methodist2Teacher.objects.filter(methodist_id=self.request.user.id)
        object_list = MethodistLessonSigns.objects.filter(teacher_id__in=method_obj.values('teacher_id'))

        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(Q(id__icontains=query) |
                                                    Q(teacher__first_name__icontains=query) |
                                                    Q(teacher__last_name__icontains=query) |
                                                    Q(teacher__middle_name__icontains=query) |
                                                    Q(teacher__work__icontains=query) |
                                                    Q(date__icontains=query)
                                                    )

        return object_list


class MethodSignsUpdateView(LoginRequiredMixin, MethodistPermissionsMixin, UpdateView):
    model = MethodistLessonSigns
    fields = ['lesson_title', 'lesson_description', 'lesson_plan', 'meet_type', 'meet_link', 'status', 'methodist_comment']
    template_name = 'core/method-signs-update.html'
    success_url = reverse_lazy('method-signs')


class MethodProfilesDetailView(LoginRequiredMixin, MethodistPermissionsMixin, TemplateView):
    template_name = 'core/method-profiles-item.html'

    def get_context_data(self, **kwargs):
        context = super(MethodProfilesDetailView, self).get_context_data()

        context['route'] = Route.objects.filter(account_id=self.kwargs['pk']).order_by('order')
        total_mark1, total_mark2, total_mark3, total_mark4 = 0, 0, 0, 0
        diagnostics_results = DiagnosticResult.objects.filter(account_id=self.kwargs['pk'])
        for res in diagnostics_results:
            total_mark1 += res.mark1
            total_mark2 += res.mark2
            total_mark3 += res.mark3
            total_mark4 += res.mark4

        context['result'] = [total_mark1, total_mark2, total_mark3, total_mark4]
        context['account'] = Account.objects.get(id=self.kwargs['pk'])
        context['lesson_signs'] = MethodistLessonSigns.objects.filter(teacher_id=self.kwargs['pk']).order_by('-id')

        return context


class MethodStatisticsView(LoginRequiredMixin, MethodistPermissionsMixin, ListView):
    template_name = 'core/method-statistic.html'
    context_object_name = 'object_list'
    model = Route
    paginate_by = 25

    def get_queryset(self):
        teachers = Methodist2Teacher.objects.filter(methodist_id=self.request.user.id)
        object_list = Route.objects.filter(account_id__in=teachers.values('teacher_id'),
                                           deadline__lt=date.today())
        return object_list


class ModerateMethodistFormView(LoginRequiredMixin, ModeratorPermissionsMixin, TemplateView):
    template_name = 'core/moderate-methodist.html'

    mun = Municipality.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ModerateMethodistFormView, self).get_context_data()

        context['formsets'] = list()

        for i in range(len(self.mun)):
            context['formsets'].append(MethodMunicipalityInlineFormset(instance=self.mun[i], prefix='mun_formset-'+str(i)))

        return context

    def post(self, *args, **kwargs):
        formsets = list()
        for i in range(len(self.mun)):
            formsets.append(MethodMunicipalityInlineFormset(data=self.request.POST,
                                                            instance=self.mun[i],
                                                            prefix='mun_formset-'+str(i)))
        for formset in formsets:
            if formset.is_valid():
                instances = formset.save(commit=False)

                for form in formset:
                    form_obj = form.save(commit=False)
                    form_obj.save()

                for obj in formset.deleted_objects:
                    print(formset.deleted_objects)
                    obj.delete()

        return HttpResponseRedirect(reverse_lazy('moderate-methodist'))