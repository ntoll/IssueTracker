# -*- coding: UTF-8 -*-
"""
Models for the Tracker application: simply represent a ticket type, and tickets.
"""
# Python
import datetime

# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext as __
from django.contrib.auth.models import User
import django.dispatch

# IssueTracker
from workflow.models import Workflow, WorkflowManager
from project.models import Project, Component

#########
# Signals
#########

# Fired whenever a new ticket is created
ticket_created = django.dispatch.Signal()
# Fired whenever a ticket is updated
ticket_updated = django.dispatch.Signal()

########
# Models
########

class TicketType(models.Model):
    """
    Represents a type of ticket that can be created in the system 
    """
    name = models.CharField(
            _('Name'),
            max_length=64
            )
    description = models.TextField(
            _('Description'),
            blank=True
            )
    workflow = models.ForeignKey(
            Workflow,
            help_text=_('The default workflow to use with a ticket of this type')
            )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name',]
        verbose_name = _('Ticket Type')
        verbose_name_plural = _('Ticket Types')

class Ticket(models.Model):
    """
    Represents a ticket in the issue tracker 
    """
    ticket_type = models.ForeignKey(TicketType)
    project = models.ForeignKey(Project)
    component = models.ForeignKey(Component)
    summary = models.CharField(
            _('Summary'),
            max_length=256,
            help_text=_('A brief summary of the ticket')
            )
    description = models.TextField(
            _('Description'),
            help_text=_('A full description of the ticket. If required please'\
                    ' note how to recreate any problems or attach evidence as'\
                    ' files.')
            )
    workflow_manager = models.ForeignKey(WorkflowManager)
    created_by = models.ForeignKey(
            User,
            related_name='tickets_created' )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
            User,
            related_name='tickets_updated')
    updated_on = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(
            User,
            related_name='tickets_assigned')

    def __unicode__(self):
        return self.name

    def save(self):
        if self.id == None:
            ticket_created.send(sender=self)
        super(Ticket, self).save()
        ticket_updated.send(sender=self)

    class Meta:
        ordering = ['-updated_on','-created_on']
        verbose_name = _('Component')
        verbose_name_plural = _('Components')

class Comment(models.Model):
    """
    Represents a comment attached to a ticket
    """
    ticket = models.ForeignKey(Ticket)
    body = models.TextField(
            _("Comment")
            )
    created_by = models.ForeignKey(
            User,
            related_name='comments')
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s (%s): %s'%(self.created_by.username,
                self.created_on.strftime('%c'),
                self.body)

    class Meta:
        ordering = ['created_on',]
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
