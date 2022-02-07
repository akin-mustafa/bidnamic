from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from bidnamic.ad_groups.views import AdGroupViewSet
from bidnamic.campaigns.views import CampaignViewSet
from bidnamic.search_terms.views import SearchTermViewSet
from bidnamic.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("campaigns", CampaignViewSet)
router.register("ad_groups", AdGroupViewSet)
router.register("search_terms", SearchTermViewSet)

app_name = "api"
urlpatterns = router.urls
