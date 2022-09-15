from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from courses.models import Account2Course
from accounts.models import Account
from diagnostics.models import DiagnosticResult
from method.models import Methodist2Teacher
from route.models import LessonSigns
from route.models import Route, RouteReflection

from django.core.paginator import Paginator


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
            context['active_lesson'] = LessonSigns.objects.get(teacher_id=self.request.user.id,
                                                               status__in=('СМОТР', 'ОДОБР'))
        except LessonSigns.DoesNotExist:
            context['active_lesson'] = None

        try:
            context['method'] = Methodist2Teacher.objects.get(teacher_id=self.request.user.id)
        except Methodist2Teacher.DoesNotExist:
            context['method'] = None

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        reflections = RouteReflection.objects.filter(route_id__in=Route.objects.filter(account_id=self.request.user.id))
        context['reflections'] = reflections

        lesson_signs = LessonSigns.objects.filter(teacher_id=self.request.user.id).order_by('id')
        paginator_lesson_signs = Paginator(lesson_signs, 10)
        page_number_lesson_signs = self.request.GET.get('lpage')
        lpage_obj = paginator_lesson_signs.get_page(page_number_lesson_signs)
        context['lpage_obj'] = lpage_obj

        course_signs = Account2Course.objects.filter(account_id=self.request.user.id).order_by('id')
        paginator_course_signs = Paginator(course_signs, 10)
        page_number_course_signs = self.request.GET.get('cpage')
        cpage_obj = paginator_course_signs.get_page(page_number_course_signs)
        context['cpage_obj'] = cpage_obj

        return self.render_to_response(context)

