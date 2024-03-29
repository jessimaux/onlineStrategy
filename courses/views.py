from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView, ListView, TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin
from onlineStrategy.permissions import ModeratorPermissionsMixin
from django.http import HttpResponseRedirect
from django.core.mail import EmailMessage
from django.db.models import Q

from .models import Course, Account2Course, CourseProgram, CourseSpeakers
from accounts.models import Account

from .forms import FilterForm, ProgramFormSet, SpeakerFormSet


class CoursesListView(LoginRequiredMixin, ListView):
    template_name = 'courses/courses.html'
    context_object_name = 'object_list'
    model = Course
    paginate_by = 10
    ordering = 'id'

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


class CourseView(LoginRequiredMixin, TemplateView):
    template_name = 'courses/course.html'

    def registration_check(self):
        return True if Account2Course.objects.filter(account_id=self.request.user.pk, course_id=self.kwargs['pk']) \
            else False

    def get_context_data(self, **kwargs):
        super(CourseView, self).get_context_data()
        context = {'form': Course.objects.get(id=self.kwargs['pk']),
                   'program': CourseProgram.objects.filter(course__id=self.kwargs['pk']),
                   'speakers': CourseSpeakers.objects.filter(course__id=self.kwargs['pk']),
                   'is_registrated': self.registration_check(),
                   }
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
        context['programformset'] = ProgramFormSet(queryset=Course.objects.none(), prefix="program_formset")
        context['speakerformset'] = SpeakerFormSet(queryset=Course.objects.none(), prefix="speaker_formset")
        return context

    def post(self, request, *args, **kwargs):
        program_formset = ProgramFormSet(request.POST, prefix="program_formset")
        speaker_formset = SpeakerFormSet(request.POST, prefix="speaker_formset")
        form = self.get_form()
        if program_formset.is_valid() and speaker_formset.is_valid() and form.is_valid():
            return self.form_valid(program_formset, speaker_formset, form)
        else:
            return self.form_invalid(program_formset, speaker_formset, form)

    def form_valid(self, program_formset, speaker_formset, form):
        form.save()
        for _form in program_formset:
            obj = _form.save(commit=False)
            obj.course_id = form.instance.id
            obj.save()
        for _form in speaker_formset:
            obj = _form.save(commit=False)
            obj.course_id = form.instance.id
            obj.save()
        return HttpResponseRedirect('/courses')

    def form_invalid(self, program_formset, speaker_formset, form):
        return self.render_to_response(self.get_context_data(form=form,
                                                             programformset=program_formset,
                                                             speakerformset=speaker_formset))


class CourseUpdateView(LoginRequiredMixin, ModeratorPermissionsMixin, UpdateView):
    model = Course
    template_name = 'courses/course_update.html'
    fields = '__all__'
    success_url = reverse_lazy('moderate-courses')

    def get_context_data(self, **kwargs):
        context = super(CourseUpdateView, self).get_context_data()
        programs = CourseProgram.objects.filter(course_id=self.kwargs['pk'])
        speakers = CourseSpeakers.objects.filter(course_id=self.kwargs['pk'])

        context['programformset'] = ProgramFormSet(queryset=programs, prefix="program_formset")
        context['speakerformset'] = SpeakerFormSet(queryset=speakers, prefix="speaker_formset")
        return context

    def post(self, request, *args, **kwargs):
        programs = CourseProgram.objects.filter(course_id=self.kwargs['pk'])
        speakers = CourseSpeakers.objects.filter(course_id=self.kwargs['pk'])

        program_formset = ProgramFormSet(request.POST, prefix="program_formset")
        speaker_formset = SpeakerFormSet(request.POST, prefix="speaker_formset")

        if program_formset.is_valid() and speaker_formset.is_valid():
            for _form in program_formset:
                obj = _form.save(commit=False)
                obj.course_id = self.kwargs['pk']
                obj.save()
            for _form in speaker_formset:
                obj = _form.save(commit=False)
                obj.course_id = self.kwargs['pk']
                obj.save()
        return super(CourseUpdateView, self).post(request, *args, **kwargs)


class CourseDeleteView(LoginRequiredMixin, ModeratorPermissionsMixin, DeleteView):
    model = Course
    success_url = reverse_lazy('moderate-courses')


class CreateAccount2CourseView(LoginRequiredMixin, CreateView):
    model = Account2Course
    fields = []
    template_name = 'courses/sign_up.html'
    success_url = reverse_lazy('index')

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
        obj = Account2Course.objects.filter(account_id=self.request.user.pk, course_id=self.kwargs['pk'])
        if obj:
            return HttpResponseRedirect(reverse_lazy('course-sign-update', args=[obj[0].id]))
        else:
            return super().get(self.request, *args, **kwargs)

    def form_valid(self, form):
        obj_account = Account.objects.get(id=self.request.user.id)
        obj_course = Course.objects.get(pk=self.kwargs['pk'])

        form.instance.account_id = self.request.user.id
        form.instance.course_id = self.kwargs['pk']
        form.save()

        # if email send is on
        """
        msg = EmailMessage(f'Запись на мероприятие {obj_course.title}',
                           f'Сообщаем Вам о записи на мероприятие',
                           'from@example.com',
                           [obj_account.email])
        msg.send()
        """
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['account'] = Account.objects.get(id=self.request.user.id)
        context['course'] = Course.objects.get(pk=self.kwargs['pk'])
        return context


class Account2CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Account2Course
    fields = []
    template_name = 'courses/sign_update.html'
    success_url = reverse_lazy('index')


