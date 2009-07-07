# -*- coding: UTF-8 -*-
# Python
import re

# Django
from django.contrib.auth.decorators import login_required, user_passes_test as check
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.http import int_to_base36, base36_to_int
from django.contrib.sites.models import Site, RequestSite
from django.template import RequestContext, Template, Context, loader
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q

# Project
from forms import RegistrationForm, SearchForm, TicketForm, AssignForm, StateForm
from models import Ticket, TicketType
from workflow.models import Workflow, Role, Participant, WorkflowManager 

###################
# Utility functions
###################
def find_tickets(searchstring):
    """ Given a search string will build an appropriate query to find the
    user(s) that match."""
    rex = re.compile(r'\W')
    normalised = rex.sub(' ', searchstring)
    if normalised:
        terms = normalised.split()
        query = Ticket.objects
        for t in terms:
            # lets try to build a Q object for all the terms
            query = query.filter(
                        Q(summary__icontains=t) | 
                        Q(description__icontains=t)
                        )
        return query
    return []

###############
# Ajax handlers
###############
@login_required
def ajax_ticket_list(request):
    """ Returns a list of matching assessors where their username or email
    address matches the query in the get url. Based on the examples at:
    http://docs.jquery.com/Plugins/Autocomplete
    """
    limit = 20 
    search_string = request.GET.get('q', None)
    results = ""
    if search_string:
        instances = find_tickets(search_string)[:limit]
        for item in instances:
            results += "%s\n"%(item.summary.strip())
    return HttpResponse(results, mimetype='text/plain')

##################
# Request handlers
##################
def home(request, *arg):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = SearchForm()
    c = RequestContext(request, {'form': form})
    return render_to_response('home.html', c)

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

@login_required
def search(request, *arg):
    """
    Returns the result of a search
    """
    if request.method == 'POST':
        form = SearchForm(request.POST)
        results = []
        if form.is_valid():
            search_string = form.cleaned_data['searchbox']
            if search_string:
                results = find_tickets(search_string)
    else:
        form = SearchForm()
        results = []
    c = RequestContext(request, {'form': form, 'results': results})
    return render_to_response('search.html', c) 

@login_required
def new_ticket(request, *arg):
    """
    For generating new tickets
    """
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            t = Ticket()
            t.ticket_type = form.cleaned_data['ticket_type']
            t.project = form.cleaned_data['project']
            t.component = form.cleaned_data['component']
            t.summary = form.cleaned_data['summary']
            t.description = form.cleaned_data['description']
            t.created_by = request.user
            t.updated_by = request.user
            # workflow related stuff
            ticket_type = t.ticket_type
            wm = WorkflowManager()
            wm.workflow = ticket_type.workflow
            wm.created_by = request.user
            wm.save()
            r = Role.objects.get(id=settings.ROLE_SUBMITTER)
            p = Participant()
            p.user = request.user
            p.role = r
            p.workflowmanager=wm
            p.save()
            t.workflow_manager=wm
            t.save()
            wm.start(p)
            # Generates a confirmation email to send to the new user
            current_site = Site.objects.get_current() 
            site_name = current_site.name
            domain = current_site.domain
            tplt = loader.get_template(settings.NEW_TICKET_EMAIL_TEMPLATE)
            c = {
                'email': request.user.email,
                'domain': domain,
                'site_name': site_name,
                'user': request.user,
                'protocol': settings.REGISTRATION_USE_HTTPS and 'https' or 'http',
                'ticket': t,
            }
            send_mail(_("Confirmation of new ticket on IssueTracker"),
                tplt.render(Context(c)), None, [request.user.email])
            
            request.user.message_set.create(message=_("The ticket has been"\
                    " successfully created."))
            return HttpResponseRedirect('/ticket/%d'%t.id)
    else:
        form = TicketForm()
    c = RequestContext(request, {'form': form})
    return render_to_response('new.html', c) 

@login_required
def ticket(request, pk):
    """
    View a ticket
    """
    ticket = get_object_or_404(Ticket, id=pk)
    if request.method == 'POST':
        assignform = AssignForm(request.POST, prefix="assign")
        stateform = StateForm(
                request.POST, 
                prefix="state",
                workflow_manager=ticket.workflow_manager
                )
        if "change" in request.POST:
            if stateform.is_valid():
                transition = stateform.cleaned_data['transition']
                p = Participant.objects.get(
                    user=request.user,
                    workflowmanager=ticket.workflow_manager
                    )
                ticket.workflow_manager.progress(
                        transition,
                        p
                        )
                request.user.message_set.create(message=_("The ticket has been"\
                    " successfully transitioned to a new state.."))
                assign_dict={}
                if ticket.assigned_to:
                    assign_dict = {'assign-assignee': ticket.assigned_to.id}
                assignform = AssignForm(assign_dict, prefix="assign")
                stateform = StateForm(
                    prefix="state", 
                    workflow_manager=ticket.workflow_manager
                    )
        elif "assign" in request.POST:
            if assignform.is_valid():
                u = assignform.cleaned_data['assignee']
                ticket.assigned_to = u 
                ticket.save()
                r = Role.objects.get(id=settings.ROLE_ASSIGNEE)
                p = Participant.objects.filter(user=u, 
                        workflowmanager=ticket.workflow_manager)
                if len(p)==1:
                    p[0].role=r
                    p[0].save()
                else:
                    p = Participant(
                        role=r, 
                        user=u,
                        workflowmanager=ticket.workflow_manager
                        )
                    p.save()
                request.user.message_set.create(message=_("The ticket has been"\
                    " successfully re-assigned."))
    else:
        assign_dict={}
        if ticket.assigned_to:
            assign_dict = {'assign-assignee': ticket.assigned_to.id}
        assignform = AssignForm(assign_dict, prefix="assign")
        stateform = StateForm(
                prefix="state", 
                workflow_manager=ticket.workflow_manager
                )
    c = RequestContext(request, {
        'ticket': ticket,
        'assignform': assignform,
        'stateform': stateform,
        })
    return render_to_response('ticket.html', c)

@login_required
def my_tickets(request, *args):
    """
    Display all tickets involving this user
    """
    results = Ticket.objects.filter(workflow_manager__participants__user=request.user)
    c = RequestContext(request, {'results': results})
    return render_to_response('my_tickets.html', c)
