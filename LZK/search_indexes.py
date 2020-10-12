from haystack import indexes

from . import models


class AbilityIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # subjects = indexes.CharField(model_attr='subject')
    # pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return models.Ability

    def index_queryset(self, using=None):
        return self.get_model().objects.exclude(depth=None).filter(public=True)


class SymptomIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # subjects = indexes.CharField(model_attr='subject')
    # pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return models.Symptom

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(public=True)


class ActivityIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # subjects = indexes.CharField(model_attr='subject')
    # pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return models.Activity

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class SkillIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # subjects = indexes.CharField(model_attr='subject')
    # pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return models.Skill

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
