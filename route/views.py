from django.contrib.auth.mixins import LoginRequiredMixin
from onlineStrategy.permissions import ModeratorPermissionsMixin
from django.views.generic import ListView, TemplateView, UpdateView, CreateView, DeleteView, FormView

from .models import RouteReflection, Manual, Route, LessonSigns
from accounts.models import Account
from diagnostics.models import DiagnosticResult
from django.db.models import Q

from .forms import OrderingForm

from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse_lazy

from .tools import negative_number_is_zero


class ManualsCreateView(LoginRequiredMixin, ModeratorPermissionsMixin, CreateView):
    model = Manual
    fields = '__all__'
    template_name = 'route/manuals-create.html'
    success_url = reverse_lazy('moderate-manuals')


class ManualsUpdateView(LoginRequiredMixin, ModeratorPermissionsMixin, UpdateView):
    model = Manual
    template_name = 'route/manuals-update.html'
    fields = '__all__'
    success_url = reverse_lazy('moderate-manuals')


class ManualsDeleteView(LoginRequiredMixin, ModeratorPermissionsMixin, DeleteView):
    model = Manual
    success_url = reverse_lazy('moderate-manuals')


class RouteManualsListView(LoginRequiredMixin, ListView):
    template_name = 'route/route-manuals.html'
    context_object_name = 'object_list'
    model = Manual
    paginate_by = 25
    ordering = 'id'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RouteManualsListView, self).get_context_data()
        try:
            profile = DiagnosticResult.objects.get(account_id=self.request.user.id)
            context['diagnostics_exists'] = True
        except DiagnosticResult.DoesNotExist:
            context['diagnostics_exists'] = False
        return context

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
                                    manual=Manual(id=kwargs['pk']))
            messages.success(request, 'Материал уже находится в вашем образовательном маршруте')
        except Route.DoesNotExist:
            Route(account=Account(id=request.user.pk),
                  manual=Manual(id=kwargs['pk'])).save()
            messages.success(request, 'Материал добавлен в ваш образовательный маршрут')
        return HttpResponseRedirect('/route')


class RouteView(LoginRequiredMixin, TemplateView):
    template_name = 'route/route.html'

    def get_context_data(self, **kwargs):
        context = super(RouteView, self).get_context_data()

        profile_route = Route.objects.filter(account_id=self.request.user.id).order_by('order')
        context['route'] = profile_route

        context['reflections_exists'] = RouteReflection.objects\
            .filter(route_id__in=profile_route).exclude(status='ОТКЛ')\
            .values_list('route_id', flat=True)

        try:
            profile = DiagnosticResult.objects.get(account_id=self.request.user.id)
            context['diagnostics_exists'] = True
        except DiagnosticResult.DoesNotExist:
            context['diagnostics_exists'] = False
            return context

        """ selection manuals """
        # TODO: improve recomendations
        '''Take unusing manuals and recommend it with evklid distance > 5'''
        using_manuals = Route.objects.filter(account_id=self.request.user.id)
        manuals = Manual.objects.exclude(id__in=using_manuals.values('manual_id'))
        context['recommendation'] = list()

        for manual in manuals:
            dist = (negative_number_is_zero(manual.mark1 - profile.mark1) ** 2 +
                    negative_number_is_zero(manual.mark2 - profile.mark2) ** 2 +
                    negative_number_is_zero(manual.mark3 - profile.mark3) ** 2 +
                    negative_number_is_zero(manual.mark4 - profile.mark4) ** 2) ** (1 / 2)
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
    template_name = 'route/route-item.html'
    model = Route
    fields = ['deadline']
    success_url = reverse_lazy('route')


class RouteReflectionCreateView(LoginRequiredMixin, CreateView):
    template_name = 'route/route-reflection-create.html'
    model = RouteReflection
    fields = ['text']
    success_url = reverse_lazy('route')

    def dispatch(self, request, *args, **kwargs):
        try:
            reflection_exists = RouteReflection.objects.get(route_id=self.kwargs['pk'])
        except RouteReflection.DoesNotExist:
            reflection_exists = None
        if reflection_exists and reflection_exists.status != 'ОТКЛ':
            return HttpResponseRedirect(reverse_lazy('route'))
        else:
            return super(RouteReflectionCreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RouteReflectionCreateView, self).get_context_data()
        context['manual'] = Manual.objects.get(id=Route.objects.get(id=self.kwargs['pk']).manual_id)
        return context

    def form_valid(self, form):
        form.instance.route_id = self.kwargs['pk']
        return super(RouteReflectionCreateView, self).form_valid(form)


class RouteReflectionUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'route/route-reflection-update.html'
    model = RouteReflection
    fields = ['text']
    success_url = reverse_lazy('route')

    def get_form(self, form_class=None):
        form = super(RouteReflectionUpdateView, self).get_form(form_class)

        if self.object.status != 'СМОТР' or self.request.user.id != self.object.route.account_id:
            for field in form:
                field.field.widget.attrs['disabled'] = True

        return form


class RouteLessonSignsCreateView(LoginRequiredMixin, CreateView):
    model = LessonSigns
    fields = ['lesson_title', 'lesson_description', 'lesson_plan', 'date', 'meet_type', 'meet_link']
    template_name = 'route/route-lesson-signs-up.html'
    success_url = reverse_lazy('index')

    '''Redirect if user have active lesson sign'''
    def dispatch(self, request, *args, **kwargs):
        try:
            active_lesson = LessonSigns.objects.get(teacher_id=self.request.user.id,
                                                    status__in=('СМОТР', 'ОДОБР'))
        except LessonSigns.DoesNotExist:
            active_lesson = None
        if active_lesson:
            return HttpResponseRedirect(reverse_lazy('index'))
        else:
            return super(RouteLessonSignsCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.teacher_id = self.request.user.id
        form.save()
        return super().form_valid(form)


class RouteLessonSignsUpdateView(LoginRequiredMixin, UpdateView):
    model = LessonSigns
    fields = ['lesson_title', 'lesson_description', 'lesson_plan', 'date', 'meet_type', 'meet_link',
              'methodist_comment']
    template_name = 'route/route-lesson-signs-update.html'
    success_url = reverse_lazy('index')
    
    def get_form(self, form_class=None):
        form = super(RouteLessonSignsUpdateView, self).get_form(form_class)

        if self.object.status != 'СМОТР' or self.request.user.id != self.object.teacher_id:
            for field in form:
                field.field.widget.attrs['disabled'] = True

        return form
