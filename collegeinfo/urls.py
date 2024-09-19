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
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#*********This is affiliation router registered by autoapi*********
from affiliation.routers.routers import router as affiliation_router
urlpatterns.append(path('api/',include(affiliation_router.urls)))
#*********This is certification router registered by autoapi*********
from certification.routers.routers import router as certification_router
urlpatterns.append(path('api/',include(certification_router.urls)))
#*********This is college router registered by autoapi*********
from college.routers.routers import router as college_router
urlpatterns.append(path('api/',include(college_router.urls)))
#*********This is collegeleveltype router registered by autoapi*********
from collegeleveltype.routers.routers import router as collegeleveltype_router
urlpatterns.append(path('api/',include(collegeleveltype_router.urls)))
#*********This is collegetype router registered by autoapi*********
from collegetype.routers.routers import router as collegetype_router
urlpatterns.append(path('api/',include(collegetype_router.urls)))
#*********This is course router registered by autoapi*********
from course.routers.routers import router as course_router
urlpatterns.append(path('api/',include(course_router.urls)))
#*********This is district router registered by autoapi*********
from district.routers.routers import router as district_router
urlpatterns.append(path('api/',include(district_router.urls)))
#*********This is event router registered by autoapi*********
from event.routers.routers import router as event_router
urlpatterns.append(path('api/',include(event_router.urls)))
#*********This is faculty router registered by autoapi*********
from faculty.routers.routers import router as faculty_router
urlpatterns.append(path('api/',include(faculty_router.urls)))
#*********This is gallery router registered by autoapi*********
from gallery.routers.routers import router as gallery_router
urlpatterns.append(path('api/',include(gallery_router.urls)))
#*********This is informationmanagement router registered by autoapi*********
from informationmanagement.routers.routers import router as informationmanagement_router
urlpatterns.append(path('api/',include(informationmanagement_router.urls)))
#*********This is level router registered by autoapi*********
from level.routers.routers import router as level_router
urlpatterns.append(path('api/',include(level_router.urls)))
#*********This is semester router registered by autoapi*********
from semester.routers.routers import router as semester_router
urlpatterns.append(path('api/',include(semester_router.urls)))
#*********This is setupemail router registered by autoapi*********
from setupemail.routers.routers import router as setupemail_router
urlpatterns.append(path('api/',include(setupemail_router.urls)))
#*********This is socialmedia router registered by autoapi*********
from socialmedia.routers.routers import router as socialmedia_router
urlpatterns.append(path('api/',include(socialmedia_router.urls)))