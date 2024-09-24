"""
URL configuration for collegeinfo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf import settings
from django.conf.urls.static import static

from coursemanagement.routers.routers import router as coursemanagement_router
from socialmedia.routers.routers import router as socialmedia_router
from setupemail.routers.routers import router as setupemail_router
from semester.routers.routers import router as semester_router
from level.routers.routers import router as level_router
from informationmanagement.routers.routers import router as informationmanagement_router
from affiliation.routers.routers import router as affiliation_router
from certification.routers.routers import router as certification_router
from college.routers.routers import router as college_router
from collegeleveltype.routers.routers import router as collegeleveltype_router
from collegetype.routers.routers import router as collegetype_router
from course.routers.routers import router as course_router
from event.routers.routers import router as event_router
from district.routers.routers import router as district_router
from faculty.routers.routers import router as faculty_router
from gallery.routers.routers import router as gallery_router

schema_view = get_schema_view(
   openapi.Info(
      title="College Info API",
      default_version='v1',
      description="College Info Backend System",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="prashantkarna21@gmail.com"),
      license=openapi.License(name="No License"),
      **{'x-logo': {'url': 'your-logo-url'}},
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/accounts/',include('accounts.urls')),
    path('api/',include(coursemanagement_router.urls)),
    path('api/',include(socialmedia_router.urls)),
    path('api/',include(setupemail_router.urls)),
    path('api/',include(semester_router.urls)),
    path('api/',include(level_router.urls)),
    path('api/',include(informationmanagement_router.urls)),
    path('api/',include(affiliation_router.urls)),
    path('api/',include(certification_router.urls)),
    path('api/',include(college_router.urls)),
    path('api/',include(collegeleveltype_router.urls)),
    path('api/',include(collegetype_router.urls)),
    path('api/',include(course_router.urls)),
    path('api/',include(district_router.urls)),
    path('api/',include(event_router.urls)),
    path('api/',include(faculty_router.urls)),
    path('api/',include(gallery_router.urls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



