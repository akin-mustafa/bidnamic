from django.contrib import admin

from bidnamic.ad_groups.models import AdGroup


@admin.register(AdGroup)
class AdGroupAdmin(admin.ModelAdmin):
    pass
