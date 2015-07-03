# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import redirect


def home(request):
    messages.add_message(request, messages.WARNING,
        'The default username & password are both "admin".')
    return redirect('admin:index')
