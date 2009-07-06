# -*- coding: UTF-8 -*-
from django.contrib.auth.decorators import login_required, user_passes_test as check
from django.utils.translation import ugettext as _
from django.shortcuts import render_to_response

def home(request, *arg):
    return render_to_response('base.html')
