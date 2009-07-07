# -*- coding: UTF-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from models import Ticket

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

class SearchForm(forms.Form):
    """
    For searching for tickets
    """
    searchbox = forms.CharField(max_length=256,
            widget=forms.TextInput(attrs={'class':'focus', 'size':'55'}),
            label='Search (use keywords)',
            required=True,
            error_messages={ 
                'required': _('Please enter something to search for') 
                }
            )

class TicketForm(forms.ModelForm):
    """
    For creating new tickets
    """
    class Meta:
        model = Ticket
        exclude = ('workflow_manager', 'created_by', 'created_on', 'updated_by',
                'updated_on', 'assigned_to')

class AssignForm(forms.Form):
    """
    For selecting who to assign the ticket to
    """
    assignee = forms.ModelChoiceField(
            queryset = User.objects.filter(is_staff=True)
            )

class StateForm(forms.Form):
    """
    For selecting the next state to move to in the workflow
    """
    def __init__(self, *args, **kwargs):
        wm = kwargs['workflow_manager']
        del kwargs['workflow_manager']
        super(StateForm, self).__init__(*args, **kwargs)
        self.fields['transition'].queryset = wm.current_state().state.transitions_from.all()

    transition = forms.ModelChoiceField(queryset = None) 
