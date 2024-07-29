from django.contrib import admin

class BaseTimeAdmin(admin.ModelAdmin):
    __fields__ = ('created', 'updated')

    def __init__(self, *args, **kwargs):
        self.list_display = self.list_display + BaseTimeAdmin.__fields__
        self.readonly_fields = self.readonly_fields + self.__fields__
        super().__init__(*args, **kwargs)

class BaseInfoAdmin(BaseTimeAdmin):
    __fields__ = ('created', 'updated', 'description')

