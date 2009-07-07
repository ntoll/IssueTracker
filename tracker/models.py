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
            _('Description')
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
            related_name='tickets_assigned',
            limit_choices_to={'is_staff': True},
            null=True
            )

    def __unicode__(self):
        return self.name

    def save(self):
        if self.id == None:
            ticket_created.send(sender=self)
        super(Ticket, self).save()
        ticket_updated.send(sender=self)

    class Meta:
        ordering = ['-updated_on','-created_on']
        verbose_name = _('Ticket')
        verbose_name_plural = _('Tickets')
