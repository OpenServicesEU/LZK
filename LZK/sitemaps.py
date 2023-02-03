from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from . import models


class StaticViewSitemap(Sitemap):
    protocol = "https"
    priority = 1.0
    changefreq = "monthly"

    def items(self):
        return [
            "index",
            "ability-list",
            "symptom-list",
            "skill-list",
        ]

    def location(self, item):
        return reverse(item)


class AbilitySitemap(Sitemap):
    protocol = "https"
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return models.Ability.objects.filter(public=True)


class SymptomSitemap(Sitemap):
    protocol = "https"
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return models.Symptom.objects.filter(public=True)


class SkillSitemap(Sitemap):
    protocol = "https"
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return models.Skill.objects.all()
