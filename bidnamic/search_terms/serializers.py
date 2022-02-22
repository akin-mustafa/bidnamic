from rest_framework import serializers

from bidnamic.search_terms.models import SearchTerm


class SearchTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchTerm
        fields = "__all__"


class TopSearchesSerializer(serializers.ModelSerializer):
    total_cost = serializers.DecimalField(decimal_places=2,
                                          max_digits=10,
                                          read_only=True,
                                          required=False)
    total_conversion_value = serializers.IntegerField(read_only=True,
                                                      required=False)
    roas = serializers.DecimalField(decimal_places=2,
                                    max_digits=10,
                                    read_only=True,
                                    required=False)
    structure_value = serializers.CharField(required=False)
    alias = serializers.CharField(required=False)

    class Meta:
        model = SearchTerm
        fields = ["search_term", "total_cost", "total_conversion_value",
                  "roas", "structure_value", "alias"]
