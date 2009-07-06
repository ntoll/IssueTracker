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

class ModelTestCase(TestCase):
        """
        Testing Models 
        """
        # Reference fixtures here
        fixtures = ['tracker_test_data']

        def test_something(self):
            pass


