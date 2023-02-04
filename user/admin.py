from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


# Register your models here.


class Admin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", 'dot', 'email', 'first_name', 'last_name'),
            },
        ),
    )


class CmpAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('dot', )


class DotAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('name', )


class InformationAdmin(admin.ModelAdmin):
    list_filter = (('date', admin.DateFieldListFilter), 'cmp')
    date_hierarchy = 'date'


class InformationDotAdmin(admin.ModelAdmin):
    list_filter = (('date', admin.DateFieldListFilter), 'dot')
    date_hierarchy = 'date'


admin.site.register(models.User, Admin)
admin.site.register(models.Dot, DotAdmin)
admin.site.register(models.Cmp, CmpAdmin)
admin.site.register(models.File)
admin.site.register(models.Information, InformationAdmin)
admin.site.register(models.InformationDot, InformationDotAdmin)
