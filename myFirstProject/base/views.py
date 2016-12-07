from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login

from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from users.forms import LoginForm
from users.models import User


class IndexView(TemplateView):
    """
    Index view
    """
    template_name = 'base/index.html'
    form = LoginForm()

    def get(self, request):
        # if request.user.is_authenticated():
        #     return HttpResponseRedirect('/')

        return render(request, self.template_name, {'login_form': self.form})

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        login_form = LoginForm()
        context['login_form'] = login_form
        return context

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
