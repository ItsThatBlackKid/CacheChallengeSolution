from .views import DocumentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', DocumentViewSet, base_name='Document')
urlpatterns = router.urls
