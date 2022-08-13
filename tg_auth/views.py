from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.signing import Signer
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from .models import UserAirtable


class Login(LoginView):
    template_name = 'tg_auth/login.html'
    success_url = reverse_lazy('user-tg')


class Logout(LogoutView):
    pass


class UserTgView(LoginRequiredMixin, TemplateView):
    template_name = 'tg_auth/user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.user.username
        context['airtable_user'] = list(UserAirtable.objects.filter(tg_username=username))[0]
        return context


def user_data(request, username):
    signer = Signer(salt='airtable')
    query = UserAirtable.objects.filter(tg_username=signer.unsign(username))
    user = next(iter(query))
    return render(request, 'tg_auth/user.html', context={'air_user': user})
