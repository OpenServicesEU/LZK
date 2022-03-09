from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _
from ordered_model.admin import OrderedModelAdmin
from reversion.admin import VersionAdmin

from . import models

admin.sites.AdminSite.site_header = _("Lernzielkatalog")
admin.sites.AdminSite.site_title = _("Administration")
admin.sites.AdminSite.index_title = _("Administration")


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + ((None, {"fields": ("university",)}),)
    add_fieldsets = BaseUserAdmin.add_fieldsets + ((None, {"fields": ("university",)}),)


@admin.register(models.Level)
class LevelAdmin(VersionAdmin):
    pass


@admin.register(models.Subject)
class SubjectAdmin(VersionAdmin):
    search_fields = ("name",)


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
    search_fields = ("name",)


@admin.register(models.StudyField)
class StudyFieldAdmin(VersionAdmin):
    pass


@admin.register(models.ModuleTrack)
class ModuleTrackAdmin(VersionAdmin):
    pass


class AbilityCommentInline(admin.TabularInline):
    model = models.AbilityComment

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(status=models.AbilityComment.ACCEPTED, feedback__active=True)


@admin.register(models.Ability)
class AbilityAdmin(VersionAdmin):
    list_display = ("name", "depth", "public")
    list_filter = (
        "public",
        "depth",
    )
    search_fields = ("name",)
    inlines = (AbilityCommentInline,)


@admin.register(models.CompetenceLevel)
class CompetenceLevelAdmin(VersionAdmin):
    pass


@admin.register(models.Activity)
class ActivityAdmin(VersionAdmin):
    pass


class SkillCommentInline(admin.TabularInline):
    model = models.SkillComment

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(status=models.SkillComment.ACCEPTED, feedback__active=True)


@admin.register(models.Skill)
class SkillAdmin(VersionAdmin):
    list_display = ("name", "activity", "clinical_traineeship_checklist")
    list_filter = ("clinical_traineeship_checklist",)
    search_fields = ("name",)
    inlines = (SkillCommentInline,)


class SymptomCommentInline(admin.TabularInline):
    model = models.SymptomComment

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(status=models.SymptomComment.ACCEPTED, feedback__active=True)


@admin.register(models.Symptom)
class SymptomAdmin(VersionAdmin):
    list_display = ("name", "public")
    list_filter = ("public",)
    search_fields = ("name",)
    inlines = (SymptomCommentInline,)


@admin.register(models.RoleModel)
class RoleModelAdmin(VersionAdmin):
    list_display = ("pk", "name")
    search_fields = ("name",)


@admin.register(models.Slide)
class SlideAdmin(OrderedModelAdmin):
    list_display = ("title", "move_up_down_links")


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "active", "datetime")
    search_fields = ("title",)


@admin.register(models.Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ("title", "active", "top")
    list_filter = ("active", "top")
    exclude = ("icon",)


@admin.register(models.Text)
class TextAdmin(OrderedModelAdmin):
    list_display = ("title", "placement")
    list_filter = ("placement",)
    search_fields = ("title", "body")

    class Media:
        js = ("ckeditor/ckeditor.js", "LZK/admin/text.js")
