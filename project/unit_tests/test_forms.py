# -*- coding: UTF-8 -*-
"""
Forms tests for Project app 

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
from project.forms import *

class FormsTestCase(TestCase):
        """
        Testing Models 
        """
        # Reference fixtures here
        fixtures = ['project_test_data']

        def test_something(self):
            pass
