# -*- coding: UTF-8 -*-
from django.contrib import admin
from models import TicketType, Ticket

class TicketTypeAdmin(admin.ModelAdmin):
    """
    TicketType administration
    """
    list_display = ['name', 'description', 'workflow']
    search_fields = ['name', 'description']
    save_on_top = True

class TicketAdmin(admin.ModelAdmin):
    """
    Ticket administration
    """
    list_display = ['summary', 'description', 'ticket_type', 'project', 
            'component', 'created_by', 'created_on', 'assigned_to']
    search_fields = ['name', 'description']
    save_on_top = True
    list_filter = ['project', 'component', 'ticket_type', 'assigned_to']

admin.site.register(TicketType, TicketTypeAdmin)
admin.site.register(Ticket, TicketAdmin)
