# -*- coding: UTF-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test as check
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.http import int_to_base36, base36_to_int
from django.contrib.sites.models import Site, RequestSite
from django.template import RequestContext, Template, Context, loader
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse

from forms import RegistrationForm

def home(request, *arg):
    return render_to_response('base.html')

def register(request, *arg):
    """ Takes care of the registration process"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            # Generates a confirmation email to send to the new user
            current_site = Site.objects.get_current() 
            site_name = current_site.name
            domain = current_site.domain
            t = loader.get_template(settings.REGISTRATION_EMAIL_TEMPLATE)
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'user': user,
                'protocol': settings.REGISTRATION_USE_HTTPS and 'https' or 'http',
            }
            send_mail(_("Registration confirmation from IssueTracker"),
                t.render(Context(c)), None, [user.email])
            # Now lets sign them on and send them to their home page
            # Lets make sure the requesting user isn't already logged in  
            if request.user.is_authenticated():
                logout(request)
            user_logged_in = authenticate(username=user.username,
                                         password=form.cleaned_data['password']) 
            login(request, user_logged_in)
            request.user.message_set.create(message=_("You have been "\
                "successfully signed up with the IssueTracker system."))
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm() 
    return render_to_response('register.html', {'form': form})

def password_done(request, *arg):
    """ Displays a friendly message when the user's password has been
    successfully changed"""
    request.user.message_set.create(message=_("Your password has been"\
        " successfully updated."))
    return HttpResponseRedirect('/')

