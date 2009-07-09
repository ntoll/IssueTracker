# -*- coding: UTF-8 -*-
"""
Models tests for Project app 

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
from project.models import *

class ModelTestCase(TestCase):
        """
        Testing Models 
        """
        # Reference fixtures here
        fixtures = ['project_test_data']

        def test_project__unicode__(self):
            p = Project.objects.get(id=1)
            self.assertEqual(u'Project X', p.__unicode__())

        def test_component__unicode__(self):
            c = Component.objects.get(id=1)
            self.assertEqual(u'Merlin Workflow Engine', c.__unicode__())
