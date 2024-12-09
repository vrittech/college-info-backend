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
from  rest_framework  import routers

from coursemanagement.routers.routers import router as coursemanagement_router
from socialmedia.routers.routers import router as socialmedia_router
# from setupemail.routers.routers import router as setupemail_router

from accounts.routers.routers import router as accounts_router
from contact.routers.routers import router as contact_router
from advertisement.routers.routers import router as advertisement_router
from duration.routers.routers import router as duration_router
from formprogress.routers.routers import router as formprogress_router
from inquiry.routers.routers import router as inquiry_router
from superadmindetails.routers.routers import router as superadmindetails_router
from requestsubmission.routers.routers import router as requestsubmission_router

# from semester.routers.routers import router as semester_router
from level.routers.routers import router as level_router
from informationmanagement.routers.routers import router as informationmanagement_router
from affiliation.routers.routers import router as affiliation_router
from certification.routers.routers import router as certification_router
# from college.routers.routers import router as college_router
# from collegeleveltype.routers.routers import router as collegeleveltype_router
from collegetype.routers.routers import router as collegetype_router
from event.routers.routers import router as event_router
from district.routers.routers import router as district_router
from faculty.routers.routers import router as faculty_router
from gallery.routers.routers import router as gallery_router
from collegemanagement.routers.routers import router as collegemanagement_router
from facilities.routers.routers import router as facilities_router
# from admissionopen.routers.routers import router as admissionopen_router
from coursesandfees.routers.routers import router as coursesandfees_router
# from location.routers.routers import router as location_router
# from preparationinquiries.routers.routers import router as preparationinquiries_router
# from collegeandcourseinquiries.routers.routers import router as collegeandcourseinquiries_router
from discipline.routers.routers import router as discipline_router


router = routers.DefaultRouter()

router.registry.extend(requestsubmission_router.registry)
router.registry.extend(coursemanagement_router.registry)
router.registry.extend(socialmedia_router.registry)
# router.registry.extend(setupemail_router.registry)
# router.registry.extend(semester_router.registry)
router.registry.extend(level_router.registry)
router.registry.extend(informationmanagement_router.registry)
router.registry.extend(affiliation_router.registry)
router.registry.extend(certification_router.registry)
# router.registry.extend(collegeleveltype_router.registry)
router.registry.extend(collegetype_router.registry)
router.registry.extend(event_router.registry)
router.registry.extend(district_router.registry)
router.registry.extend(faculty_router.registry)
router.registry.extend(gallery_router.registry)
router.registry.extend(collegemanagement_router.registry)
router.registry.extend(facilities_router.registry)
# router.registry.extend(admissionopen_router.registry)
router.registry.extend(coursesandfees_router.registry)
# router.registry.extend(location_router.registry)
# router.registry.extend(preparationinquiries_router.registry)
# router.registry.extend(collegeandcourseinquiries_router.registry)

router.registry.extend(discipline_router.registry)
router.registry.extend(accounts_router.registry)
router.registry.extend(contact_router.registry)
router.registry.extend(advertisement_router.registry)
router.registry.extend(duration_router.registry)
router.registry.extend(formprogress_router.registry)
router.registry.extend(inquiry_router.registry)
router.registry.extend(superadmindetails_router.registry)

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
    path('api/', include(router.urls)),
    path('api/',include('accountsmanagement.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/accounts/',include('accounts.urls')),
    # path('api/',include(requestsubmission_router.urls)),
    # path('api/',include(coursemanagement_router.urls)),
    # path('api/',include(socialmedia_router.urls)),
    # path('api/',include(setupemail_router.urls)),
    # path('api/',include(semester_router.urls)),
    # path('api/',include(level_router.urls)),
    # path('api/',include(informationmanagement_router.urls)),
    # path('api/',include(affiliation_router.urls)),
    # path('api/',include(certification_router.urls)),
    # path('api/',include(college_router.urls)),
    # path('api/',include(collegeleveltype_router.urls)),
    # path('api/',include(collegetype_router.urls)),
    # path('api/',include(district_router.urls)),
    # path('api/',include(event_router.urls)),
    # path('api/',include(faculty_router.urls)),
    # path('api/',include(gallery_router.urls)),
    # path('api/',include(collegemanagement_router.urls)),
    # path('api/',include(facilities_router.urls)),
    # path('api/',include(admissionopen_router.urls)),
    # path('api/',include(coursesandfees_router.urls)),
    # path('api/',include(location_router.urls)),
    # path('api/',include(preparationinquiries_router.urls)),
    # path('api/',include(collegeandcourseinquiries_router.urls))
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # for development