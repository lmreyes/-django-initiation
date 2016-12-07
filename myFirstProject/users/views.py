from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView

from registration.backends.simple.views import RegistrationView
from registration.backends.hmac.views import RegistrationView as ActivationRegistrationView

from base.decorators import anonymous_required
from .forms import LoginForm, UserRegisterForm
from .models import User


class LoginView(View):
    template_name = 'registration/login.html'
    form = LoginForm()

    def get(self, request):
        # if request.user.is_authenticated():
        #     return HttpResponseRedirect('/')

        return render(request, self.template_name, {'login_form': self.form})

    def post(self, request):
        context = {}
        self.form = LoginForm(request.POST or None)

        if request.POST and self.form.is_valid():
            user_email = request.POST['email']
            user_password = request.POST['password']
            username = User.objects.get(email=user_email).username
            user = authenticate(username=username, password=user_password)
            auth_login(request, user)
            context['authenticated'] = request.user.is_authenticated()
            if context['authenticated']:
                context['username'] = request.user.username
                return redirect('home')

        context.update({'login_form': self.form})
        return render(request, self.template_name, context)


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        auth_logout(request)

        return HttpResponseRedirect(settings.LOGIN_URL)


@method_decorator(anonymous_required(redirect_url='index'), name='dispatch')
class UserActivationRegisterView(ActivationRegistrationView):
    form_class = UserRegisterForm


@method_decorator(anonymous_required(redirect_url='index'), name='dispatch')
class UserNormalRegisterView(RegistrationView):
    form_class = UserRegisterForm


@method_decorator(login_required(login_url='login'), name='dispatch')
class HomeView(TemplateView):
    """
    Home view
    """
    template_name = 'users/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['authenticated'] = self.request.user.is_authenticated()
        if context['authenticated']:
            context['user_detail'] = User.objects.get(username=self.request.user)
        return context
