# -*- coding: UTF-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    """ For user registration"""
    username = forms.CharField(max_length=30,
            widget=forms.TextInput(attrs={'class':'focus'}),
            label=_('Username'))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                widget=forms.PasswordInput)
    email = forms.EmailField(label=_('Email Address'), 
            help_text=_('e.g. name@company.com'))
    first_name = forms.CharField(max_length=30,
            label=_('First name'))
    last_name = forms.CharField(max_length=30,
            label=_('Last name'))

    def clean_username(self):
        """ Make sure we don't have any duplicate usernames """
        uname = self.cleaned_data['username']
        if User.objects.filter(username__exact=uname):
            raise forms.ValidationError(
                    _("A user with this username already exists"))
        return uname

    def clean_email(self):
        """ Make sure we don't have any duplicate emails"""
        email = self.cleaned_data['email']
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError(
                    _("A user with this email address already exists"))
        return email 

    def clean_password2(self): 
        password = self.cleaned_data.get("password", "") 
        password2 = self.cleaned_data["password2"] 
        if password != password2: 
            raise forms.ValidationError(_("The two password fields didn't"\
                    " match.")) 
        return password2
