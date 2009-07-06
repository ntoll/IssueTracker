# -*- coding: UTF-8 -*-
from django.contrib import admin
from models import Project, Component 

class ProjectAdmin(admin.ModelAdmin):
    """
    Project administration
    """
    list_display = ['name', 'description', 'slug']
    search_fields = ['name', 'description']
    save_on_top = True

class ComponentAdmin(admin.ModelAdmin):
    """
    Component administration
    """
    list_display = ['name', 'description', 'slug']
    search_fields = ['name', 'description']
    save_on_top = True

admin.site.register(Project, ProjectAdmin)
admin.site.register(Component, ComponentAdmin)
