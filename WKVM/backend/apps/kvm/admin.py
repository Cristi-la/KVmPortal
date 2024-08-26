from django.contrib import admin
from apps.kvm.models import Auth, Tag, Hypervisor, VM
from utils.admin import BaseInfoAdmin, BaseTimeAdmin

class AuthAdmin(admin.ModelAdmin):
    list_display = ('username', 'port')
    search_fields = ('username',)


class TagAdmin(BaseInfoAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)


class HypervisorAdmin(BaseInfoAdmin):
    list_display = ('hostname', 'mgt_ip')
    search_fields = ('hostname', 'mgt_ip')
    list_filter = ('tags',)


class VMAdmin(BaseInfoAdmin):
    list_display = ('name', 'hypervisor', 'vcpu', 'memory')
    search_fields = ('name', 'mgt_ip', 'vcpu', 'memory')
    list_filter = ('hypervisor', 'tags')


admin.site.register(Auth, AuthAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Hypervisor, HypervisorAdmin)
admin.site.register(VM, VMAdmin)