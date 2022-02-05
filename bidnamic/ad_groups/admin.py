from django.contrib import admin

from bidnamic.ad_groups.models import AdGroup


@admin.register(AdGroup)
class AdGroupAdmin(admin.ModelAdmin):
    list_display = ["id", "campaign_id", "alias", "status"]
