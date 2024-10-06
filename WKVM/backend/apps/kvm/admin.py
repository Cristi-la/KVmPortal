from django.contrib import admin
from apps.kvm.models import Auth, Tag, Hypervisor, VM, XMLData, KeyFile, VMInterface
from utils.admin import BaseInfoAdmin, BaseTimeAdmin, BaseTabularInline
from django.urls import reverse
from django.utils.html import format_html

# --------------------------------------------------------
# Auth classes
# --------------------------------------------------------
@admin.register(KeyFile)
class KeyFileAdmin(BaseInfoAdmin):
    list_display = ('id', 'path',)
    search_fields = ('id', 'key_file')
    
    def path(self, obj):
        return obj.key_file.path
    
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Auth)
class AuthAdmin(BaseInfoAdmin):
    list_display = ('id', 'username', 'driver', 'transport', 'port')
    search_fields = ('id', 'username', 'driver', 'transport', 'port')
    readonly_fields = ('password',)

    def has_change_permission(self, request, obj=None):
        return False

# --------------------------------------------------------
# Utility classes
# --------------------------------------------------------
@admin.register(Tag)
class TagAdmin(BaseInfoAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)

@admin.register(XMLData)
class XMLDataAdmin(BaseInfoAdmin):
    list_display = ('xml_type', 'xml_hash')
    readonly_fields = ('xml_hash',)
    fieldsets = (
        (None, {
            'fields': ('xml_type', 'raw_xml', 'xml_hash')
        }),
    )
    
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False
    
# --------------------------------------------------------
# Inline classes
# --------------------------------------------------------

class TagInline(admin.TabularInline):
    model = Hypervisor.tags.through
    extra = 0
    verbose_name = "Tag"
    verbose_name_plural = "Tags"

class XMLDataInline(BaseTabularInline):
    model = Hypervisor.xmls.through
    verbose_name = "XML Data"
    verbose_name_plural = "XML Data"

    def _name(self, obj):
        return self.create_link(obj.pk, obj.xmldata.__str__(), obj.xmldata.__class__)

class VMInline(BaseTabularInline):
    model = VM
    fields = ('vcpu', 'memory', 'state')  
    readonly_fields = ('vcpu', 'memory', 'state')

@admin.register(Hypervisor)
class HypervisorAdmin(BaseInfoAdmin):
    list_display = ('id', 'hostname', 'mgt_ip', 'get_uri', 'auth',)
    search_fields = ('hostname', 'mgt_ip',)
    list_filter = ('auth',)
    inlines = [TagInline, VMInline, XMLDataInline,]
    exclude = ('tags', 'xmls')

    def get_uri(self, obj):
        return obj.get_uri()

    get_uri.short_description = 'URI'


class VMTagInline(admin.TabularInline):
    model = VM.tags.through
    extra = 0
    verbose_name = "Tag"
    verbose_name_plural = "Tags"

class VMXMLDataInline(BaseTabularInline):
    model = VM.xmls.through
    verbose_name = "XML Data"
    verbose_name_plural = "XML Data"
    
    def _name(self, obj):
        return self.create_link(obj.pk, obj.xmldata.__str__(), obj.xmldata.__class__)

class VMInterfaceInline(BaseTabularInline):
    model = VMInterface
    verbose_name = "Interface"
    verbose_name_plural = "Interfaces"
    fields = ('mac', )  
    readonly_fields = ( 'mac', )

# --------------------------------------------------------

@admin.register(VM)
class VMAdmin(BaseInfoAdmin):
    list_display = ('id', 'name', 'hypervisor_link', 'vcpu', 'memory', 'state')
    search_fields = ('name', 'hypervisor__hostname')
    list_filter = ('state', 'hypervisor')
    inlines = [VMTagInline, VMXMLDataInline, VMInterfaceInline]
    exclude = ('tags', 'xmls')

    def hypervisor_link(self, obj):
        url = reverse('admin:kvm_hypervisor_change', args=[obj.hypervisor.pk])
        return format_html('<a href="{}">{}</a>', url, obj.hypervisor.hostname)

    hypervisor_link.short_description = 'Hypervisor'


# --------------------------------------------------------

@admin.register(VMInterface)
class VMInterface(BaseInfoAdmin):
    list_display = ('id', 'vm', 'mac', 'model_type', 'source_network', 'source_type')
    search_fields = ('vm__name', 'mac', 'model_type', 'source_network', 'source_type')

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False