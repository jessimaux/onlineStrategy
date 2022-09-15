from django.contrib.auth.mixins import LoginRequiredMixin
from onlineStrategy.permissions import ModeratorPermissionsMixin

from django.views.generic import ListView, TemplateView, UpdateView, FormView
from django.http import HttpResponseRedirect

from courses.models import Course, Account2Course
from accounts.models import Account
from route.models import Manual
from core.models import Municipality
from diagnostics.models import Diagnostic
from django.db.models import Q

from .forms import MethodMunicipalityInlineFormset
from courses.forms import AccountCourseInListForm, SignFormSet
from accounts.forms import AccountUpdateForm

from django.urls import reverse_lazy


class ModerateCoursesListView(LoginRequiredMixin, ModeratorPermissionsMixin, ListView):
    template_name = 'moderate/moderate-courses.html'
    context_object_name = 'object_list'
    model = Course
    paginate_by = 10
    ordering = 'id'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(title__icontains=query)
            return object_list
        else:
            return super(ModerateCoursesListView, self).get_queryset()


class ModerateAccount2CourseListView(LoginRequiredMixin, ModeratorPermissionsMixin, FormView):
    template_name = 'moderate/moderate-courses-signs.html'
    form_class = AccountCourseInListForm

    def get_context_data(self, **kwargs):
        context = super(ModerateAccount2CourseListView, self).get_context_data()
        object_list = Account2Course.objects.filter(course_id=self.kwargs['pk'])

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
            return super(ModerateAccount2CourseListView, self).get(request, *args, **kwargs)

    def form_valid(self, formset):
        for _form in formset:
            obj = _form.save(commit=False)
            # event = Events.objects.create(user=Account(id=self.request.user.pk),
            #                               content_object=AccountCourse(id=obj.id),
            #                               event_type='EDIT')
            # e_fields = EventEditedFields.objects.create(event=event,
            #                                             fields=list(obj.tracker.changed().keys()),
            #                                             prev=obj.tracker.previous('status'),
            #                                             current=obj.get_status_display())
            obj.save()
        return super(ModerateAccount2CourseListView, self).get(self.request)


class ModerateManualsListView(LoginRequiredMixin, ModeratorPermissionsMixin, ListView):
    template_name = 'moderate/moderate-manuals.html'
    context_object_name = 'object_list'
    model = Manual
    paginate_by = 25
    ordering = 'id'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(Q(title__icontains=query) |
                                                    Q(author__icontains=query))
            return object_list
        else:
            return super().get_queryset()


class ModerateMethodistFormView(LoginRequiredMixin, ModeratorPermissionsMixin, TemplateView):
    template_name = 'moderate/moderate-methodist.html'

    mun = Municipality.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ModerateMethodistFormView, self).get_context_data()
        temp = list()
        temp_mun = list()

        for i in range(len(self.mun)):
            temp.append(MethodMunicipalityInlineFormset(instance=self.mun[i], prefix='mun_formset-' + str(i)))
            temp_mun.append(self.mun[i].name)

        context['formsets'] = zip(temp_mun, temp)
        return context

    def post(self, *args, **kwargs):
        formsets = list()
        for i in range(len(self.mun)):
            formsets.append(MethodMunicipalityInlineFormset(data=self.request.POST,
                                                            instance=self.mun[i],
                                                            prefix='mun_formset-' + str(i)))
        for formset in formsets:
            if formset.is_valid():
                instances = formset.save(commit=False)

                for form in formset:
                    form_obj = form.save(commit=False)
                    if form_obj.method_id:
                        form_obj.save()

                for obj in formset.deleted_objects:
                    obj.delete()

        return HttpResponseRedirect(reverse_lazy('moderate-methodist'))


class ModerateDiagnosticsListView(LoginRequiredMixin, ModeratorPermissionsMixin, ListView):
    template_name = 'moderate/moderate-diagnostics.html'
    context_object_name = 'object_list'
    model = Diagnostic
    paginate_by = 25
    ordering = 'id'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(Q(title__icontains=query))
            return object_list
        else:
            return super().get_queryset()


class ModerateAccountsListView(LoginRequiredMixin, ModeratorPermissionsMixin, ListView):
    template_name = 'moderate/moderate-profiles.html'
    context_object_name = 'object_list'
    model = Account
    paginate_by = 50
    ordering = 'id'

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
            return super(ModerateAccountsListView, self).get_queryset()


class ModerateAccountView(LoginRequiredMixin, ModeratorPermissionsMixin, UpdateView):
    model = Account
    template_name = 'moderate/moderate-profile-card.html'
    form_class = AccountUpdateForm