# -*- coding: UTF-8 -*-
"""
Models tests for Tracker app 

Author: Nicholas H.Tollervey

"""
# python
import datetime
import sys

# django
from django.test.client import Client
from django.test import TestCase
from django.contrib.auth.models import User

# project
from tracker.models import *
from project.models import *
from workflow.models import Workflow, WorkflowManager

class ModelTestCase(TestCase):
        """
        Testing Models 
        """
        # Reference fixtures here
        fixtures = ['project_test_data']

        def test_ticket_type__unicode__(self):
            tt = TicketType()
            tt.name = 'Test1'
            tt.description = "A description"
            w = Workflow.objects.get(id=1)
            tt.workflow = w
            tt.save()
            self.assertEquals(u'Test1', tt.__unicode__())

        def test_ticket__unicode__(self):
            tt = TicketType()
            tt.name = 'Test1'
            tt.description = "A description"
            w = Workflow.objects.get(id=1)
            tt.workflow = w
            tt.save()
            p = Project.objects.get(id=1)
            c = Component.objects.get(id=1)
            u = User.objects.get(id=1)
            wm = WorkflowManager()
            wm.workflow = w
            wm.created_by = u 
            wm.save()
            t = Ticket()
            t.ticket_type = tt
            t.project = p
            t.component = c
            t.summary = "Summary"
            t.description = "Description"
            t.created_by = u
            t.updated_by = u
            t.workflow_manager = wm
            t.save()
            self.assertEquals(u'Summary', t.__unicode__())

