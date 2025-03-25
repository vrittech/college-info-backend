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
            "add_customuser", "change_customuser", "view_customuser",
            "add_college", "change_college", "view_college",
            "add_collegegallery", "change_collegegallery", "delete_collegegallery", "view_collegegallery",
            "add_collegefaqs", "change_collegefaqs", "delete_collegefaqs", "view_collegefaqs",
            "add_facility", "change_facility", "delete_facility", "view_facility",
            "add_coursesandfees", "change_coursesandfees", "delete_coursesandfees", "view_coursesandfees",
            "add_contact", "change_contact", "view_contact",
            "add_requestsubmission", "change_requestsubmission", "view_requestsubmission","view_inquiry",
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

@receiver(post_save, sender=Group)
def ensure_college_admin_group_exists(sender, instance, created, **kwargs):
    if instance.name.lower() != "college admin":
        # Try to get or create "College Admin" group
        college_admin_group, is_created = Group.objects.get_or_create(name="College Admin")

        if is_created:
            # If created, assign permissions
            permissions_to_assign = [
                "add_customuser", "change_customuser", "view_customuser",
                "add_college", "change_college", "view_college",
                "add_collegegallery", "change_collegegallery", "delete_collegegallery", "view_collegegallery",
                "add_collegefaqs", "change_collegefaqs", "delete_collegefaqs", "view_collegefaqs",
                "add_facility", "change_facility", "delete_facility", "view_facility",
                "add_coursesandfees", "change_coursesandfees", "delete_coursesandfees", "view_coursesandfees",
                "add_contact", "change_contact", "view_contact",
                "add_requestsubmission", "change_requestsubmission", "view_requestsubmission",
                "view_inquiry"
            ]

            for codename in permissions_to_assign:
                try:
                    permission = Permission.objects.get(codename=codename)
                    college_admin_group.permissions.add(permission)
                except Permission.DoesNotExist:
                    print(f"Warning: Permission '{codename}' does not exist.")