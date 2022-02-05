from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from bidnamic.campaigns.views import CampaignViewSet
from bidnamic.users.api.views import UserViewSet
from bidnamic.ad_groups.views import AdGroupViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("campaigns", CampaignViewSet)
router.register("ad_groups", AdGroupViewSet)

app_name = "api"
urlpatterns = router.urls
