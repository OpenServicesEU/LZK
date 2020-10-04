from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from ordered_model.admin import OrderedModelAdmin
from reversion.admin import VersionAdmin
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
class LevelAdmin(VersionAdmin):
    pass


@admin.register(models.Subject)
class SubjectAdmin(VersionAdmin):
    pass


class ContactInline(admin.TabularInline):
    model = models.Contact


@admin.register(models.University)
class UniversityAdmin(VersionAdmin):
    inlines = (ContactInline,)


@admin.register(models.System)
class SystemAdmin(VersionAdmin):
    pass


@admin.register(models.UFID)
class UFIDAdmin(VersionAdmin):
    pass


@admin.register(models.StudyField)
class StudyFieldAdmin(VersionAdmin):
    pass


@admin.register(models.ModuleTrack)
class ModuleTrackAdmin(VersionAdmin):
    pass


@admin.register(models.Objective)
class ObjectiveAdmin(VersionAdmin):
    pass


@admin.register(models.CompetenceLevel)
class CompetenceLevelAdmin(VersionAdmin):
    pass


@admin.register(models.Activity)
class ActivityAdmin(VersionAdmin):
    pass


@admin.register(models.Skill)
class SkillAdmin(VersionAdmin):
    pass


@admin.register(models.Symptom)
class SymptomAdmin(VersionAdmin):
    pass


@admin.register(models.Slide)
class SlideAdmin(OrderedModelAdmin):
    list_display = ("title", "move_up_down_links")


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "active", "datetime")
