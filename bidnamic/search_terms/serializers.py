from rest_framework import serializers

from bidnamic.search_terms.models import SearchTerm


class SearchTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchTerm
        fields = "__all__"
