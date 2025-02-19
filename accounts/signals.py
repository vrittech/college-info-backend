from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from accounts.models import College, CustomUser  # Update with actual models

@receiver(m2m_changed, sender=College.users.through)  # Ensure the related field is correct
def assign_college_admin_group(sender, instance, action, pk_set, **kwargs):
    """
    When a user is assigned to a college, assign them to the 'College Admin' group.
    Only applicable if the user is assigned to at least one college.
    """
    if action == "post_add":  # Ensure it's triggered only after assignment

        # Ensure 'College Admin' group exists
        college_admin_group, created = Group.objects.get_or_create(name="College Admin")

        if created:
            # Define required permissions
            permissions_to_assign = [
                # Request Submission - CRU
                "add_request_submission", "change_request_submission", "view_request_submission",

                # College Management - CRU
                "add_college", "change_college", "view_college",

                # Courses and Fees - CRUD
                "add_courses_and_fees", "change_courses_and_fees", "delete_courses_and_fees", "view_courses_and_fees",

                # Facilities - CRUD
                "add_facility", "change_facility", "delete_facility", "view_facility",

                # College Gallery - CRUD
                "add_college_gallery", "change_college_gallery", "delete_college_gallery", "view_college_gallery",

                # FAQ about College - CRUD
                "add_college_faqs", "change_college_faqs", "delete_college_faqs", "view_college_faqs",

                # Inquiry - View Only
                "view_inquiry",

                # Contact Us - CRU
                "add_contact", "change_contact", "view_contact",

                # Own Profile - CRU
                "add_custom_user", "change_custom_user", "view_custom_user",
            ]

            # Assign permissions to the group
            for perm_name in permissions_to_assign:
                try:
                    permission = Permission.objects.get(codename=perm_name)
                    college_admin_group.permissions.add(permission)
                except Permission.DoesNotExist:
                    print(f"Permission '{perm_name}' not found.")

        # Assign users to the 'College Admin' group only if they are assigned to a college
        for user_id in pk_set:
            user = CustomUser.objects.get(pk=user_id)

            # Ensure the user has at least one college
            if user.colleges.exists():  # Assuming 'colleges' is the related_name
                user.groups.add(college_admin_group)  # Add to group
                user.save()
