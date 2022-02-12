from rest_framework import serializers

from . import models


class SkillSerializer(serializers.HyperlinkedModelSerializer):
    target = serializers.URLField(source="get_absolute_url")

    class Meta:
        model = models.Skill
        fields = ['url', 'name', "clinical_traineeship_checklist", 'target']
        extra_kwargs = {
            'url': {'view_name': 'api:skill-detail'}
        }
