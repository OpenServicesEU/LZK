from rest_framework import serializers

from . import models


class SkillSerializer(serializers.HyperlinkedModelSerializer):
    target = serializers.SerializerMethodField()

    class Meta:
        model = models.Skill
        fields = ['url', 'name', "clinical_traineeship_checklist", 'target']
        extra_kwargs = {
            'url': {'view_name': 'api:skill-detail'}
        }

    def get_target(self, obj):
        request = self.context.get("request")
        path = obj.get_absolute_url()
        if not request:
            return path
        return request._request.build_absolute_uri(path)
