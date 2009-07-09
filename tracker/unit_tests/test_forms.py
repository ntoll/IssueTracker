# -*- coding: UTF-8 -*-
"""
Forms tests for Tracker app 

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
from tracker.forms import *
from tracker.models import *
from workflow.models import Role, Workflow, WorkflowManager, Participant

class FormsTestCase(TestCase):
        """
        Testing Models 
        """
        # Reference fixtures here
        fixtures = ['project_test_data']

        def test_registration_form_validation(self):
            data = {
                    "username": "fred",
                    "password": "password",
                    "password2": "password",
                    "email": "fred@company.com",
                    "first_name": "fred",
                    "last_name": "blogs"
                    }
            f = RegistrationForm(data)
            # the good case
            self.assertEquals(True, f.is_valid(), f.errors)

            # existing username
            data['username'] = 'alice'
            f = RegistrationForm(data)
            self.assertEquals(False, f.is_valid())
            data['username'] = 'fred'

            # mismatch passwords
            data['password2'] = 'drowssap'
            f = RegistrationForm(data)
            self.assertEquals(False, f.is_valid())
            data['password2'] = 'password'

            # duplicate emails
            data['email'] = 'alice.smith@acme.com'
            f = RegistrationForm(data)
            self.assertEquals(False, f.is_valid())
            data['email'] = 'fred@company.com'

        def test_state_form_init(self):
            """
            As the __init__ method is overridden - we need to check the form is
            set up properly
            """
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
            r = Role.objects.get(id=1)
            p = Participant(
                    role=r,
                    user=u,
                    workflowmanager=wm
                    )
            p.save()
            wm.start(p)
            sf = StateForm(workflow_manager=wm)
            self.assertEqual(sf.fields['transition'].queryset[0],
                    wm.current_state().state.transitions_from.all()[0])
