from rest_framework.routers import DefaultRouter
from ..viewsets.gallery_viewsets import galleryViewsets

router = DefaultRouter()

router.register('gallery', galleryViewsets, basename="galleryViewsets")
