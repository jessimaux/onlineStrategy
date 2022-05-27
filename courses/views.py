from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, UpdateView, CreateView, DeleteView, ListView, TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin
from onlineStrategy.permissions import ModeratorPermissionsMixin
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.db.models import Q

from .models import Course, AccountCourse, CourseProgram, CourseSpeakers
from accounts.models import Account

from .forms import AccountCourseInListForm, SignFormSet, FilterForm, ProgramFormSet


class CoursesListView(LoginRequiredMixin, ModeratorPermissionsMixin, ListView):
    template_name = 'courses/courses.html'
    context_object_name = 'object_list'
    model = Course

    def get_queryset(self):
        query = self.request.GET.get('search')
        filter_profile = self.request.GET.get('profile')
        filter_subject = self.request.GET.get('subject')

        if query or filter_subject or filter_profile:
            return Course.objects.filter(Q(title__icontains=query) & Q(profile__icontains=filter_profile) &
                                     Q(subject__icontains=filter_subject))
        else:
            return super(CoursesListView, self).get_queryset()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['form'] = FilterForm(initial={
            'search': self.request.GET.get('search', ''),
            'profile': self.request.GET.get('profile', ''),
            'subject': self.request.GET.get('subject', ''),
        })

        return context


class CourseCreateView(LoginRequiredMixin, ModeratorPermissionsMixin, CreateView):
    model = Course
    fields = '__all__'
    template_name = 'courses/course_create.html'

    def __init__(self):
        super(CourseCreateView, self).__init__()
        self.object = None

    def get_context_data(self, **kwargs):
        context = super(CourseCreateView, self).get_context_data(**kwargs)
        context['formset'] = ProgramFormSet(queryset=Course.objects.none())
        return context

    def post(self, request, *args, **kwargs):
        formset = ProgramFormSet(request.POST)
        form = self.get_form()
        if formset.is_valid() and form.is_valid():
            return self.form_valid(formset, form)
        else:
            return self.form_invalid(formset, form)

    def form_valid(self, formset, form):
        form.save()
        for _form in formset:
            obj = _form.save(commit=False)
            obj.course_id = form.instance.id
            obj.save()
        return HttpResponseRedirect('/courses')

    def form_invalid(self, formset, form):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))


class CourseUpdateView(LoginRequiredMixin, ModeratorPermissionsMixin, UpdateView):
    model = Course
    template_name = 'courses/course_update.html'
    fields = '__all__'


class CourseView(LoginRequiredMixin, ModeratorPermissionsMixin, TemplateView):
    template_name = 'courses/course.html'

    def registration_check(self):
        return True if AccountCourse.objects.filter(account_id=self.request.user.pk, course_id=self.kwargs['pk']) \
            else False

    def get_context_data(self, **kwargs):
        super(CourseView, self).get_context_data()
        context = {'form': Course.objects.get(id=self.kwargs['pk']),
                   'program': CourseProgram.objects.filter(course__id=self.kwargs['pk']),
                   'speakers': CourseSpeakers.objects.filter(course__id=self.kwargs['pk']),
                   'is_registrated': self.registration_check(),
                   }
        return context


class CourseDeleteView(LoginRequiredMixin, ModeratorPermissionsMixin, DeleteView):
    model = Course
    success_url = reverse_lazy('moderate-courses')


class AccountCourseListView(LoginRequiredMixin, ModeratorPermissionsMixin, FormView):
    template_name = 'courses/course_view.html'
    form_class = AccountCourseInListForm

    def get_context_data(self, **kwargs):
        context = super(AccountCourseListView, self).get_context_data()
        object_list = AccountCourse.objects.filter(course_id=self.kwargs['pk'])

        query = self.request.GET.get('q')
        if query:
            object_list = object_list.filter(Q(account__last_name__icontains=query) |
                                             Q(account__first_name__icontains=query) |
                                             Q(account__middle_name__icontains=query) |
                                             Q(account__subject_of_country__icontains=query) |
                                             Q(account__municipality__icontains=query)
                                             )

        formset = SignFormSet(queryset=object_list)
        context['management_form'] = formset.management_form
        context['object_list'] = zip(object_list, formset)
        context['course_title'] = Course.objects.get(id=self.kwargs['pk']).title
        return context

    def post(self, request, *args, **kwargs):
        formset = SignFormSet(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)
        else:
            return super(AccountCourseListView, self).get(request, *args, **kwargs)

    def form_valid(self, formset):
        formset.save()
        return super(AccountCourseListView, self).get(self.request)


class CreateAccountCourseView(LoginRequiredMixin, CreateView):
    model = AccountCourse
    fields = []
    template_name = 'courses/sign_up.html'

    # function check empty field in profile
    '''
    empty_field_flag = False
    def check_empty_field(self):
        obj = Account.objects.get(id=self.request.user.id)
        for field in Account._meta.fields:
            if not getattr(obj, field.name) and field.name != 'staff' and field.name != 'superuser' \
                    and field.name != 'moderator':
                print(field.name)
                return False
        return True
    '''

    def get(self, request, *args, **kwargs):
        obj = AccountCourse.objects.filter(account_id=self.request.user.pk, course_id=self.kwargs['pk'])
        if obj:
            return HttpResponseRedirect(reverse_lazy('sign', args=[obj[0].id]))
        else:
            return super().get(self.request, *args, **kwargs)

    def form_valid(self, form):
        obj_account = Account.objects.get(id=self.request.user.id)
        obj_course = Course.objects.get(pk=self.kwargs['pk'])

        form.instance.account_id = self.request.user.id
        form.instance.course_id = self.kwargs['pk']
        form.save()

        # if email send is on
        msg = EmailMessage(f'Запись на мероприятие {obj_course.title}',
                           f'Сообщаем Вам о записи на мероприятие',
                           'from@example.com',
                           [obj_account.email])
        msg.send()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['account'] = Account.objects.get(id=self.request.user.id)
        context['course'] = Course.objects.get(pk=self.kwargs['pk'])
        #context['empty_fields'] = self.check_empty_field()
        return context


class AccountCourseUpdateView(LoginRequiredMixin, UpdateView):
    model = AccountCourse
    fields = []
    template_name = 'courses/sign_update.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['account'] = Account.objects.get(id=self.request.user.id)
        context['course'] = AccountCourse.objects.get(pk=self.kwargs['pk']).course
        return context