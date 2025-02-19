from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from accounts.models import College, CustomUser  # Update with actual model paths

@receiver(post_save, sender=CustomUser)
def assign_college_admin_group(sender, instance, created, **kwargs):
    """
    When a user is assigned a college, assign them to the 'College Admin' group.
    Ensures only assigned users become College Admins.
    """
    if instance.college:  # Check if the user is assigned to a college
        # Ensure the 'College Admin' group exists
        college_admin_group, created = Group.objects.get_or_create(name="College Admin")

        if created:
            # Define necessary permissions
            permissions_to_assign = [
                "add_request_submission", "change_request_submission", "view_request_submission",
                "add_college", "change_college", "view_college",
                "add_courses_and_fees", "change_courses_and_fees", "delete_courses_and_fees", "view_courses_and_fees",
                "add_facility", "change_facility", "delete_facility", "view_facility",
                "add_college_gallery", "change_college_gallery", "delete_college_gallery", "view_college_gallery",
                "add_college_faqs", "change_college_faqs", "delete_college_faqs", "view_college_faqs",
                "view_inquiry",
                "add_contact", "change_contact", "view_contact",
                "add_custom_user", "change_custom_user", "view_custom_user",
            ]

            # Assign permissions to the group
            for perm_name in permissions_to_assign:
                try:
                    permission = Permission.objects.get(codename=perm_name)
                    college_admin_group.permissions.add(permission)
                except Permission.DoesNotExist:
                    print(f"Permission '{perm_name}' does not exist.")

        # Assign the user to the 'College Admin' group
        instance.groups.add(college_admin_group)
