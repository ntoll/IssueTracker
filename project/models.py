# -*- coding: UTF-8 -*-
"""
Models for the Project application: simply represent a project, its components
and who is in charge of what.
"""
from django.db import models
from django.utils.translation import ugettext_lazy as _, ugettext as __
from django.contrib.auth.models import User
import django.dispatch
import datetime

#########
# Signals
#########

# Fired whenever a new component is created
component_created = django.dispatch.Signal()
# Fired when a user is associated with a project or one of its components
responsibility_define = django.dispatch.Signal()

########
# Models
########

class Project(models.Model):
    """
    Represents a high level project
    """
    name = models.CharField(
            _('Project Name'),
            max_length=64
            )
    description = models.TextField(
            _('Description'),
            blank=True
            )
    slug = models.SlugField(
            _('Slug field'),
            help_text=_('To be used in the URL')
            )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name',]
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        permissions = ( ('can_administer_projects','Can administer projects'),)

class Component(models.Model):
    """
    Represents a component in a project
    """
    name = models.CharField(
            _('Component Name'),
            max_length=64
            )
    description = models.TextField(
            _('Description'),
            blank=True
            )
    slug = models.SlugField(
            _('Slug field'),
            help_text=_('To be used in the URL')
            )

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name',]
        verbose_name = _('Component')
        verbose_name_plural = _('Components')
