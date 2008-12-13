from django.contrib import admin
from noan.repository.models import *

class PackageInline(admin.TabularInline):
    model = Package
    extra = 0

class UpdateInline(admin.TabularInline):
    model = Update
    extra = 0

class SourceAdmin(admin.ModelAdmin):
    inlines = [PackageInline, UpdateInline]
    list_filter = ['distribution']
    search_fields = ['name']

class BinaryAdmin(admin.ModelAdmin):
    search_fields = ['update__source__name']

admin.site.register(Distribution)
admin.site.register(Source, SourceAdmin)
admin.site.register(Binary, BinaryAdmin)
