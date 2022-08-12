from django import forms


class LoginLikeForm(forms.Form):

    login = forms.CharField(max_length=255, required=True, help_text='Your telegram username')
    password = forms.CharField(max_length=255, required=True)
