import logging

from django.db import models
from psqlextra.manager import PostgresManager
from django_extensions.db.models import TimeStampedModel
from django_extensions.db.fields import RandomCharField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from markupfield.fields import MarkupField
from django.dispatch import receiver
from ordered_model.models import OrderedModel
from uuid import uuid4

from .utils import Uuid4Upload
from .validators import FileValidator
from .conf import settings

logger = logging.getLogger(__name__)


class User(AbstractUser):
    university = models.ForeignKey(
        "University",
        verbose_name=_("University"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


class University(TimeStampedModel):
    name = models.CharField(max_length=512, verbose_name=_("Name"))
    url = models.URLField()
    logo = models.FileField(
        upload_to=Uuid4Upload,
        validators=(FileValidator(mimetypes=["image/svg+xml"], extensions=["svg"]),),
    )

    class Meta:
        verbose_name = _("University")
        verbose_name_plural = _("Universities")
        ordering = ("name",)

    def __str__(self):
        return self.name


class Contact(models.Model):
    university = models.ForeignKey(
        "University", verbose_name=_("University"), on_delete=models.CASCADE
    )
    salutation = models.TextField()
    email = models.EmailField()


class Level(TimeStampedModel):
    id = models.CharField(max_length=128, primary_key=True, verbose_name=_("Acronym"))
    name = models.CharField(max_length=512, verbose_name=_("Name"))

    objects = PostgresManager()

    class Meta:
        verbose_name = _("Level")
        verbose_name_plural = _("Levels")
        ordering = ("id",)

    def __str__(self):
        return f"{self.name} ({self.id})"


class Subject(TimeStampedModel):
    id = models.CharField(max_length=128, primary_key=True, verbose_name=_("Acronym"))
    name = models.CharField(max_length=512, verbose_name=_("Name"))

    objects = PostgresManager()

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")
        ordering = ("id",)

    def __str__(self):
        return f"{self.name} ({self.id})"


class System(models.Model):
    id = models.CharField(max_length=128, primary_key=True, verbose_name=_("Acronym"))
    name = models.CharField(max_length=512, verbose_name=_("Name"))

    objects = PostgresManager()

    class Meta:
        verbose_name = _("System")
        verbose_name_plural = _("Systems")
        ordering = ("name",)

    def __str__(self):
        return self.name


class UFID(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=512, verbose_name=_("Name"))

    objects = PostgresManager()

    class Meta:
        verbose_name = _("UFID")
        verbose_name_plural = _("UFIDs")
        ordering = ("id",)

    def __str__(self):
        return f"{self.name} ({self.id})"


class StudyField(models.Model):
    id = models.CharField(max_length=128, primary_key=True, verbose_name=_("Acronym"))
    name = models.CharField(max_length=512, verbose_name=_("Name"))

    objects = PostgresManager()

    class Meta:
        verbose_name = _("Study field")
        verbose_name_plural = _("Study fields")
        ordering = ("name",)

    def __str__(self):
        return self.name


class ModuleTrack(models.Model):
    name = models.CharField(max_length=512, verbose_name=_("Educational objective"))
    university = models.ForeignKey("University", on_delete=models.CASCADE)

    objects = PostgresManager()

    class Meta:
        verbose_name = _("Module track")
        verbose_name_plural = _("module tracks")
        ordering = ("name",)

    def __str__(self):
        return f"{self.university}: {self.name}"


class Objective(TimeStampedModel):
    name = models.CharField(max_length=512, verbose_name=_("Educational objective"))
    depth = models.PositiveSmallIntegerField(
        choices=[(1, "1"), (2, "2")], verbose_name=_("Depth"), blank=True, null=True
    )
    levels = models.ManyToManyField("Level")
    subjects = models.ManyToManyField("Subject")
    subject_related = models.BooleanField(verbose_name=_("Subject related"))
    systems = models.ManyToManyField("System")
    ufids = models.ManyToManyField("UFID")
    study_field = models.ForeignKey(
        "StudyField", on_delete=models.CASCADE, blank=True, null=True
    )
    module_tracks = models.ManyToManyField("ModuleTrack")
    public = models.BooleanField(default=False)

    objects = PostgresManager()

    class Meta:
        verbose_name = _("Objective")
        verbose_name_plural = _("Objectives")
        ordering = ("name",)

    def __str__(self):
        return self.name


class Symptom(TimeStampedModel):
    name = models.CharField(max_length=512, verbose_name=_("Symptom"))
    subjects = models.ManyToManyField("Subject")

    objects = PostgresManager()

    class Meta:
        verbose_name = _("Symptom")
        verbose_name_plural = _("Symptoms")
        ordering = ("name",)

    def __str__(self):
        return self.name


class CompetenceLevel(OrderedModel):
    id = models.CharField(max_length=128, primary_key=True, verbose_name=_("Acronym"))
    name = models.CharField(max_length=512, verbose_name=_("Name"))
    short = models.CharField(max_length=128, verbose_name=_("Short"))
    description = models.TextField(default='', blank=True)

    class Meta(OrderedModel.Meta):
        verbose_name = _("Competence level")
        verbose_name_plural = _("Competence levels")

    def __str__(self):
        return self.short or self.name


class Activity(models.Model):
    name = models.CharField(max_length=512, verbose_name=_("Name"))
    competence_level = models.ForeignKey("CompetenceLevel", on_delete=models.CASCADE)

    objects = PostgresManager()

    class Meta:
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")
        ordering = ("name",)
        constraints = (models.UniqueConstraint(fields=("name",), name="unique_name"),)

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=512, verbose_name=_("Name"))
    activity = models.ForeignKey("Activity", on_delete=models.CASCADE)

    objects = PostgresManager()

    class Meta:
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")
        ordering = ("name",)

    def __str__(self):
        return self.name


class Feedback(models.Model):
    university = models.ForeignKey("University", on_delete=models.CASCADE)
    subject = models.ForeignKey("Subject", on_delete=models.CASCADE)
    secret = RandomCharField(length=32, unique=True, editable=False)

    class Meta:
        verbose_name = _("Feedback")
        verbose_name_plural = _("Feedbacks")

    def __str__(self):
        return f"{self.university}: {self.subject}"

    @staticmethod
    @receiver(models.signals.pre_save, sender="LZK.Feedback")
    def pre_save(sender, instance, raw, **kwargs):
        if raw:
            return
        if instance.pk:
            return
        instance.secret = str(uuid4())


class Comment(TimeStampedModel):
    feedback = models.ForeignKey("Feedback", on_delete=models.CASCADE)
    objective = models.ForeignKey("Objective", on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    comment = models.TextField()

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return self.objective


class Slide(OrderedModel):
    title = models.CharField(max_length=128)
    description = MarkupField(markup_type="restructuredtext")
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to=Uuid4Upload)

    class Meta(OrderedModel.Meta):
        verbose_name = _("Slide")
        verbose_name_plural = _("Slides")

    def __str__(self):
        return self.title


class News(TimeStampedModel):
    title = models.CharField(max_length=128)
    body = MarkupField(markup_type="restructuredtext")
    datetime = models.DateTimeField(auto_now_add=True)
    active = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = _("News")
        verbose_name_plural = _("News")
        ordering = (
            "-datetime",
        )

    def __str__(self):
        return self.title
