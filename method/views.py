from django.contrib.auth.mixins import LoginRequiredMixin
from onlineStrategy.permissions import MethodistPermissionsMixin

from django.views.generic import ListView, TemplateView, UpdateView, CreateView, DeleteView, FormView

from accounts.models import Account
from .models import Methodist2Teacher
from route.models import LessonSigns, Route, RouteReflection
from diagnostics.models import DiagnosticResult
from courses.models import Account2Course
from django.db.models import Q

from django.urls import reverse_lazy
from django.core.paginator import Paginator

from datetime import date


class MethodView(LoginRequiredMixin, MethodistPermissionsMixin, TemplateView):
    template_name = 'method/method.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        method_obj = Methodist2Teacher.objects.filter(methodist_id=self.request.user.id)
        lesson_signs = LessonSigns.objects.filter(teacher_id__in=method_obj.values('teacher_id')).order_by('id')
        paginator_lesson_signs = Paginator(lesson_signs, 10)
        page_number_lesson_signs = self.request.GET.get('lpage')
        lpage_obj = paginator_lesson_signs.get_page(page_number_lesson_signs)
        context['lpage_obj'] = lpage_obj

        route_ids = Route.objects.filter(account_id__in=method_obj.values('teacher_id'))
        reflections = RouteReflection.objects.filter(route_id__in=route_ids.values('id'))
        context['reflections'] = reflections

        teachers = Methodist2Teacher.objects.filter(methodist_id=self.request.user.id)
        iom_deadline = Route.objects.filter(account_id__in=teachers.values('teacher_id'),
                                            deadline__lt=date.today()).order_by('id')
        paginator_iom_deadline = Paginator(iom_deadline, 10)
        page_number_iom_deadline = self.request.GET.get('iompage')
        iompage_obj = paginator_iom_deadline.get_page(page_number_iom_deadline)
        context['iompage_obj'] = iompage_obj

        return self.render_to_response(context)


class MethodProfilesListView(LoginRequiredMixin, MethodistPermissionsMixin, ListView):
    template_name = 'method/method-profiles.html'
    context_object_name = 'object_list'
    model = Methodist2Teacher
    paginate_by = 50
    ordering = 'id'

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


class MethodProfilesDetailView(LoginRequiredMixin, MethodistPermissionsMixin, TemplateView):
    template_name = 'method/method-profiles-item.html'

    def get_context_data(self, **kwargs):
        context = super(MethodProfilesDetailView, self).get_context_data()

        context['route'] = Route.objects.filter(account_id=self.kwargs['pk']).order_by('order')
        try:
            context['method'] = Methodist2Teacher.objects.get(teacher_id=self.kwargs['pk'])
        except Methodist2Teacher.DoesNotExist:
            context['method'] = None

        total_mark1, total_mark2, total_mark3, total_mark4 = 0, 0, 0, 0
        diagnostics_results = DiagnosticResult.objects.filter(account_id=self.kwargs['pk'])
        for res in diagnostics_results:
            total_mark1 += res.mark1
            total_mark2 += res.mark2
            total_mark3 += res.mark3
            total_mark4 += res.mark4

        context['result_exists'] = diagnostics_results.exists()
        context['result'] = [total_mark1, total_mark2, total_mark3, total_mark4]
        context['account'] = Account.objects.get(id=self.kwargs['pk'])
        context['lesson_signs'] = LessonSigns.objects.filter(teacher_id=self.kwargs['pk']).order_by('-id')

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        reflections = RouteReflection.objects.filter(route_id__in=Route.objects.filter(account_id=self.kwargs['pk']))
        context['reflections'] = reflections

        lesson_signs = LessonSigns.objects.filter(teacher_id=self.kwargs['pk']).order_by('id')
        paginator_lesson_signs = Paginator(lesson_signs, 10)
        page_number_lesson_signs = self.request.GET.get('lpage')
        lpage_obj = paginator_lesson_signs.get_page(page_number_lesson_signs)
        context['lpage_obj'] = lpage_obj

        course_signs = Account2Course.objects.filter(account_id=self.kwargs['pk']).order_by('id')
        paginator_course_signs = Paginator(course_signs, 10)
        page_number_course_signs = self.request.GET.get('cpage')
        cpage_obj = paginator_course_signs.get_page(page_number_course_signs)
        context['cpage_obj'] = cpage_obj

        return self.render_to_response(context)


# No need, but archive it
'''
class MethodLessonSignsListView(LoginRequiredMixin, MethodistPermissionsMixin, ListView):
    template_name = 'method/method-signs.html'
    context_object_name = 'object_list'
    model = LessonSigns
    paginate_by = 25
    ordering = 'id'

    def get_queryset(self):
        method_obj = Methodist2Teacher.objects.filter(methodist_id=self.request.user.id)
        object_list = LessonSigns.objects.filter(teacher_id__in=method_obj.values('teacher_id'))

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
'''


class MethodLessonSignsUpdateView(LoginRequiredMixin, MethodistPermissionsMixin, UpdateView):
    model = LessonSigns
    fields = ['status', 'methodist_comment']
    template_name = 'method/method-signs-update.html'
    success_url = reverse_lazy('method')


class MethodReflectionUpdateView(LoginRequiredMixin, MethodistPermissionsMixin, UpdateView):
    model = RouteReflection
    fields = ['status', 'commentary']
    template_name = 'method/method-reflections-update.html'
    success_url = reverse_lazy('method')

    def form_valid(self, form):
        if form.cleaned_data['status'] == 'ПОДТВ':
            obj = Route.objects.get(id=self.object.route_id)
            obj.status = 'ЗАКР'
            obj.save()
        return super(MethodReflectionUpdateView, self).form_valid(form)