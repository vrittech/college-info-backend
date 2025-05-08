# from accounts.models import CustomUser
# from collegemanagement.models import College,CollegeGallery
# from advertisement.models import Advertisement
# from affiliation.models import Affiliation
# from certification.models import Certification
# from coursemanagement.models import Course,CourseCurriculumFile
# from event.models import EventGallery,Event,EventOrganizer
# from facilities.models import Facility,CollegeFacility
# from gallery.models import Gallery
# from informationmanagement.models import InformationGallery,Information,InformationFiles,InformationTagging,InformationCategory
# from level.models import Level,SubLevel
# from popup.models import Popup
# from socialmedia.models import SocialMedia,CollegeSocialMedia




# def extract_files():
#     model_config = [
#         {"model": College, "fields": ["dp_image", "banner_image"]},
#         {"model": University, "fields": ["logo", "image"]}
#     ]
    
#     for config in model_config:
#         for instance in config["model"].objects.all():
#             for field_name in config["fields"]:
#                 file_field = getattr(instance, field_name, None)
#                 if file_field and file_field.name:  # Check if file exists
#                     BucketFile.objects.create(
#                         file=file_field,
#                         content_type=getattr(file_field, 'content_type', None),
#                         object_id=instance.id,
#                         # size and url will be auto-populated by save()
#                     )