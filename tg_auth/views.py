from django.core.signing import Signer
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView
from .forms import LoginLikeForm
from .models import UserRecord


class LoginView(FormView):
    template_name = 'tg_auth/login.html'
    form_class = LoginLikeForm

    def form_valid(self, form):
        user_login = form.cleaned_data['login']
        user_password = form.cleaned_data['password']
        query = UserRecord.objects.filter(tg_username=user_login, password=user_password)
        user_inst = next(iter(query))
        if user_inst:
            self.signer = user_inst.signer
            return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('user_data', kwargs={'username': self.signer})


def user_data(request, username):
    signer = Signer(salt='airtable')
    query = UserRecord.objects.filter(tg_username=signer.unsign(username))
    user = next(iter(query))
    return render(request, 'tg_auth/user.html', context={'air_user': user})
