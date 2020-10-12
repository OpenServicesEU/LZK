import logging
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import RandomCharField
from django_extensions.db.models import TimeStampedModel
from markupfield.fields import MarkupField
from ordered_model.models import OrderedModel
from psqlextra.manager import PostgresManager

from .conf import settings
from .utils import Uuid4Upload
from .validators import FileValidator

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
    name = models.CharField(max_length=512, verbose_name=_("Module track"))
    university = models.ForeignKey("University", on_delete=models.CASCADE)

    objects = PostgresManager()

    class Meta:
        verbose_name = _("Module track")
        verbose_name_plural = _("module tracks")
        ordering = ("name",)

    def __str__(self):
        return f"{self.university}: {self.name}"


class Ability(TimeStampedModel):
    name = models.CharField(max_length=512, verbose_name=_("Ability"))
    depth = models.PositiveSmallIntegerField(
        choices=[(1, "1"), (2, "2")], verbose_name=_("Depth"), blank=True, null=True
    )
    levels = models.ManyToManyField("Level")
    subjects = models.ManyToManyField("Subject")
    subject_related = models.BooleanField(verbose_name=_("Subject related"))
    systems = models.ManyToManyField("System", blank=True)
    ufids = models.ManyToManyField("UFID")
    study_field = models.ForeignKey(
        "StudyField", on_delete=models.CASCADE, blank=True, null=True
    )
    module_tracks = models.ManyToManyField("ModuleTrack", blank=True)
    public = models.BooleanField(default=False)

    objects = PostgresManager()

    class Meta:
        verbose_name = _("Ability")
        verbose_name_plural = _("Abilities")
        ordering = ("name",)

    def get_absolute_url(self):
        return reverse("ability-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class Symptom(TimeStampedModel):
    name = models.CharField(max_length=512, verbose_name=_("Symptom"))
    subjects = models.ManyToManyField("Subject")
    public = models.BooleanField(default=False)

    objects = PostgresManager()

    class Meta:
        verbose_name = _("Symptom")
        verbose_name_plural = _("Symptoms")
        ordering = ("name",)

    def get_absolute_url(self):
        return reverse("symptom-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class CompetenceLevel(OrderedModel):
    id = models.CharField(max_length=128, primary_key=True, verbose_name=_("Acronym"))
    name = models.CharField(max_length=512, verbose_name=_("Name"))
    short = models.CharField(max_length=128, verbose_name=_("Short"))
    description = models.TextField(default="", blank=True)

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

    def get_absolute_url(self):
        return reverse("activity-detail", kwargs={"pk": self.pk})

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

    def get_absolute_url(self):
        return reverse("skill-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name


class Feedback(TimeStampedModel):
    university = models.ForeignKey("University", on_delete=models.CASCADE)
    subjects = models.ManyToManyField("Subject")
    activities = models.ManyToManyField("Activity")
    secret = RandomCharField(length=32, unique=True, editable=False)
    active = models.BooleanField(default=True, verbose_name=_("Active"))
    notes = MarkupField(markup_type="restructuredtext", verbose_name=_("Notes"))

    class Meta:
        verbose_name = _("Feedback")
        verbose_name_plural = _("Feedbacks")

    def __str__(self):
        return f"{self.university}: {self.created}"

    @staticmethod
    @receiver(models.signals.pre_save, sender="LZK.Feedback")
    def pre_save(sender, instance, raw, **kwargs):
        if raw:
            return
        if instance.pk:
            return
        instance.secret = str(uuid4())


class Comment(TimeStampedModel):
    OPEN = "open"
    DISCARDED = "discarded"
    ACCEPTED = "accepted"
    STATUS_CHOICES = (
        (OPEN, _("Open")),
        (DISCARDED, _("Discarded")),
        (ACCEPTED, _("Accepted")),
    )

    feedback = models.ForeignKey("Feedback", on_delete=models.CASCADE)
    status = models.CharField(
        max_length=32, choices=STATUS_CHOICES, default=OPEN, null=True
    )
    comment = models.TextField()

    class Meta:
        abstract = True
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")


class AbilityComment(Comment):
    ability = models.ForeignKey("Ability", on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("comment-ability", kwargs={"pk": self.ability.pk})


class SymptomComment(Comment):
    symptom = models.ForeignKey("Symptom", on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("comment-symptom", kwargs={"pk": self.symptom.pk})


class SkillComment(Comment):
    skill = models.ForeignKey("Skill", on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("comment-skill", kwargs={"pk": self.skill.pk})


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
        ordering = ("-datetime",)

    def __str__(self):
        return self.title


class Download(TimeStampedModel):
    title = models.CharField(max_length=128)
    body = MarkupField(markup_type="restructuredtext")
    active = models.BooleanField(default=True, verbose_name=_("Active"))
    file = models.FileField(upload_to="uploads/")

    class Meta:
        verbose_name = _("Download")
        verbose_name_plural = _("Downloads")

    def __str__(self):
        return self.title


class Text(OrderedModel):

    ABILITIES = "abilities"
    SYMPTOMS = "symptoms"
    SKILLS = "skills"
    FEEDBACK_EMAIL = "feedback-email"
    PLACEMENT_CHOICES = (
        (ABILITIES, _("Abilities")),
        (SYMPTOMS, _("Symptoms")),
        (SKILLS, _("Skills")),
        (FEEDBACK_EMAIL, _("Feedback (Email)")),
    )

    title = models.CharField(max_length=128)
    body = MarkupField(markup_type="restructuredtext")
    placement = models.CharField(
        max_length=32, choices=PLACEMENT_CHOICES, default=ABILITIES,
    )
    order_with_respect_to = "placement"

    class Meta:
        verbose_name = _("Text")
        verbose_name_plural = _("Texts")

    def __str__(self):
        return f"{self.title} ({self.placement})"
