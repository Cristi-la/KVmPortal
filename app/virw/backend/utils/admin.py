from collections.abc import Sequence
from django.contrib import admin
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html

class BaseTimeAdmin(admin.ModelAdmin):
    __readonly_fields__ = ('created', 'updated')
    __fields__ = __readonly_fields__

    def __init__(self, *args, **kwargs):
        self.list_display += BaseTimeAdmin.__fields__
        self.readonly_fields += self.__readonly_fields__
        super().__init__(*args, **kwargs)

class BaseInfoAdmin(BaseTimeAdmin):
    __readonly_fields__ = ('created', 'updated')
    __fields__ = (*__readonly_fields__, 'description')


class BaseTabularInline(admin.TabularInline):
    extra = 0
    can_delete = False
    __readonly_fields__ = ('pk', '_name',)
    __fields__ = __readonly_fields__

    def __init__(self, *args, **kwargs):
        if self.fields:
            self.fields = self.__fields__ + self.fields
        else:
            self.fields = self.__fields__

        if self.readonly_fields:
            self.readonly_fields = self.__readonly_fields__ + self.readonly_fields
        else:
            self.readonly_fields = self.__readonly_fields__

        super().__init__(*args, **kwargs)

    def has_add_permission(self, request, obj=None):
        return False
    
    def create_link(self, pk, text, model):
        if not pk:
            return "N/A"
        
        app_label = model._meta.app_label
        model_name = model._meta.model_name
        
        url = reverse(f'admin:{app_label}_{model_name}_change', args=[pk])
        return format_html('<a href="{}">{}</a>', url, text)

    def _name(self, obj):
        return self.create_link(obj.pk, str(obj), obj.__class__)
        
