from rest_framework.routers import DefaultRouter
from ..viewsets.gallery_viewsets import galleryViewsets
from ..viewsets.album_viewsets import albumViewsets

router = DefaultRouter()

router.register('gallery', galleryViewsets, basename="galleryViewsets")
router.register('album', albumViewsets, basename="albumViewsets")
