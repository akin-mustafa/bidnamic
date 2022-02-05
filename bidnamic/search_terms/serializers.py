from rest_framework import serializers

from bidnamic.ad_groups.models import AdGroup


class SearchTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdGroup
        fields = "__all__"
