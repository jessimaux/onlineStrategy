from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.views import View
from django.contrib.auth.views import LoginView, FormView
from django.views.generic import UpdateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm, AccountUpdateForm, AccountPasswordResetForm
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from .models import Account
from django.contrib import messages
from onlineStrategy.permissions import AuthenticationPermissionsMixin
from django.urls import reverse_lazy

from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView


class AuthView(LoginView):
    template_name = 'accounts/auth.html'


class RegView(AuthenticationPermissionsMixin, FormView):
    template_name = 'accounts/reg.html'
    form_class = RegisterForm
    success_url = 'index'

    def form_valid(self, form):
        user = form.save()
        email = form.cleaned_data.get('email')
        current_site = get_current_site(self.request)
        mail_subject = 'Регистрация в цифровой экосистеме ГАУДПО ЛО ИРО | ' + str(current_site)
        message = render_to_string('accounts/acc_activate_email.html', {
            'user': self.request.user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        email = EmailMessage(
            mail_subject, message, to=[email]
        )
        email.send()
        messages.success(self.request, 'Пожалуйста, подтвердите ваш email адрес для завершения регистрации')
        return redirect('index')


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    template_name = 'accounts/profile.html'

    form_class = AccountUpdateForm

    def get_object(self, queryset=None):
        obj = super(AccountUpdateView, self).get_object(queryset)
        if not self.request.user or self.request.user.pk != obj.pk:
            raise Http404()
        return obj


class AccountActivateView(AuthenticationPermissionsMixin, View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(self.request, user)
            # TODO: need message.success for confirm
            return redirect('index')
        else:
            return HttpResponse('Activation link is invalid!')


class AccountPasswordResetView(AuthenticationPermissionsMixin, PasswordResetView):
    form_class = AccountPasswordResetForm
    success_url = reverse_lazy('password_reset')

    def form_valid(self, form):
        messages.success(self.request, 'Ссылка для сброса пароля успешно отправлена!')
        return super(AccountPasswordResetView, self).form_valid(form)


class AccountPasswordResetConfirmView(AuthenticationPermissionsMixin, PasswordResetConfirmView):
    post_reset_login = True


class AccountPasswordResetCompleteView(AuthenticationPermissionsMixin, PasswordResetCompleteView):
    pass


class AccountPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('password_change')

    def form_valid(self, form):
        messages.success(self.request, 'Пароль успешно изменен!')
        return super(AccountPasswordChangeView, self).form_valid(form)
