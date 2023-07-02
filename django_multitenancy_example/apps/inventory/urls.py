from rest_framework.routers import DefaultRouter
from .views import (LocationViewSet, InventoryViewSet, CategoryViewSet, TagViewSet,
                    BrandViewSet, ModelViewSet, DocumentViewSet, ImageViewSet)

router = DefaultRouter()
router.register('location', LocationViewSet, basename='location')
router.register('inventory', InventoryViewSet, basename='inventory')
router.register('category', CategoryViewSet, basename='category')
router.register('tag', TagViewSet, basename='tag')
router.register('brand', BrandViewSet, basename='brand')
router.register('model', ModelViewSet, basename='model')
router.register('document', DocumentViewSet, basename='document')
router.register('image', ImageViewSet, basename='image')
urlpatterns = router.urls
