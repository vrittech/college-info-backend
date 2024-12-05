# import django_filters
# from django.db.models import Q
# from ..models import CustomUser
# from django.contrib.auth.models import Group


# class CustomUserFilter(django_filters.FilterSet):
#     first_name = django_filters.CharFilter(field_name="first_name", lookup_expr="icontains")
#     last_name = django_filters.CharFilter(field_name="last_name", lookup_expr="icontains")
#     position = django_filters.CharFilter(method='filter_by_multiple_positions')
#     # department = django_filters.ModelMultipleChoiceFilter(
#     #     field_name="department",
#     #     queryset=CustomUser.department.field.related_model.objects.all(),
#     #     to_field_name="id",  # Change to "name" if filtering by department name
#     # )
#     groups = django_filters.ModelMultipleChoiceFilter(
#         field_name="groups",
#         queryset=Group.objects.all(),
#         to_field_name="id",  # Change to "name" if filtering by group name
#     )
#     is_staff = django_filters.BooleanFilter()
#     is_active = django_filters.BooleanFilter()
#     created_date_gte = django_filters.DateFilter(
#         field_name="created_at", lookup_expr="gte", label="Created Date (From)"
#     )
#     created_date_lte = django_filters.DateFilter(
#         field_name="created_at", lookup_expr="lte", label="Created Date (To)"
#     )
#     email = django_filters.CharFilter(method='filter_by_multiple_emails')

#     class Meta:
#         model = CustomUser
#         fields = {
#             "username": ["exact", "icontains"],
#         }

#     def filter_by_multiple_positions(self, queryset, name, value):
#         """
#         Custom filter to handle multiple positions. Accepts comma-separated values.
#         """
#         if value:
#             positions = value.split(',')  # Split comma-separated positions
#             return queryset.filter(position__in=positions)
#         return queryset

#     def filter_by_multiple_emails(self, queryset, name, value):
#         """
#         Custom filter to handle multiple emails. Accepts comma-separated values.
#         """
#         if value:
#             emails = value.split(',')  # Split comma-separated emails
#             return queryset.filter(email__in=emails)
#         return queryset


