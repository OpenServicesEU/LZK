from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from ordered_model.admin import OrderedModelAdmin
from . import models
from django.utils.translation import ugettext_lazy as _


admin.sites.AdminSite.site_header = _("Lernzielkatalog")
admin.sites.AdminSite.site_title = _("Administration")
admin.sites.AdminSite.index_title = _("Administration")


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('university',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('university',)}),
    )


@admin.register(models.Level)
class LevelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


class ContactInline(admin.TabularInline):
    model = models.Contact


@admin.register(models.University)
class UniversityAdmin(admin.ModelAdmin):
    inlines = (ContactInline,)


@admin.register(models.System)
class SystemAdmin(admin.ModelAdmin):
    pass


@admin.register(models.UFID)
class UFIDAdmin(admin.ModelAdmin):
    pass


@admin.register(models.StudyField)
class StudyFieldAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ModuleTrack)
class ModuleTrackAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Objective)
class ObjectiveAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CompetenceLevel)
class CompetenceLevelAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Activity)
class ActivityAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Skill)
class SkillAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Symptom)
class SymptomAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Slide)
class SlideAdmin(OrderedModelAdmin):
    list_display = ("title", "move_up_down_links")


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "active", "datetime")
