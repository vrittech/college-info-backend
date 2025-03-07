import django_filters
from accounts.models import CustomUser

class CustomUserFilter(django_filters.FilterSet):
    """
    Filter class for CustomUser model excluding image fields.
    Allows filtering by email, phone, college, is_verified, etc.
    """

    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    # full_name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    phone = django_filters.CharFilter(lookup_expr='icontains')
    position = django_filters.NumberFilter()
    is_active = django_filters.BooleanFilter()
    is_verified = django_filters.BooleanFilter()
    college = django_filters.NumberFilter(field_name="college__id")  # Filter by college ID
    social_media = django_filters.CharFilter(method='filter_social_media')
    groups = django_filters.CharFilter(method='filter_groups')
    user_permissions = django_filters.CharFilter(method='filter_permissions')
    
    # ✅ Using `lte` and `gte` for date filtering
    created_date__gte = django_filters.DateFilter(field_name="created_date", lookup_expr="gte")
    created_date__lte = django_filters.DateFilter(field_name="created_date", lookup_expr="lte")
    updated_date__gte = django_filters.DateFilter(field_name="updated_date", lookup_expr="gte")
    updated_date__lte = django_filters.DateFilter(field_name="updated_date", lookup_expr="lte")

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'position',
            'is_active', 'is_verified', 'college', 'social_media', 'groups',
            'user_permissions', 'created_date__gte', 'created_date__lte',
            'updated_date__gte', 'updated_date__lte'
        ]

    def filter_social_media(self, queryset, name, value):
        """
        Filter users based on social media name.
        Example: ?social_media=Facebook
        """
        return queryset.filter(social_media__name__icontains=value)

    def filter_groups(self, queryset, name, value):
        """
        Filter users by group name.
        Example: ?groups=Admin
        """
        return queryset.filter(groups__name__icontains=value)

    def filter_permissions(self, queryset, name, value):
        """
        Filter users by permission name.
        Example: ?user_permissions=can_view_college
        """
        return queryset.filter(user_permissions__codename__icontains=value)
