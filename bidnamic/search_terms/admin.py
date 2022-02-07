from django.contrib import admin

# Register your models here.
from bidnamic.search_terms.models import SearchTerm


@admin.register(SearchTerm)
class SearchTermAdmin(admin.ModelAdmin):
    list_display = [
        "date",
        "ad_group",
        "campaign",
        "clicks",
        "cost",
        "conversion_value",
        "conversions",
        "search_term",
    ]
