from django.apps import AppConfig


class AccountsmanagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accountsmanagement'

    def ready(self) -> None:
        import accountsmanagement.action
