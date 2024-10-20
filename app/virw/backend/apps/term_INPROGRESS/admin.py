from django.contrib import admin
from apps.term.models import Session
from  utils.admin import BaseTimeAdmin

# class SessionAdmin(BaseTimeAdmin):
#     list_display = ('id', 'content_object', 'status', *BaseTimeAdmin.__fields__)
#     search_fields = ('status', 'output')
#     list_filter = ('status', 'content_type')
    
#     def get_queryset(self, request):
#         queryset = super().get_queryset(request)
#         queryset = queryset.select_related('content_type')
#         return queryset


# admin.site.register(Session, SessionAdmin)