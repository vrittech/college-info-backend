from django.db import models
from django.apps import apps
from django.utils.functional import lazy

# Function to fetch model choices dynamically
def get_all_models():
    return [(model.__name__, model.__name__) for model in apps.get_models()]

# Use lazy evaluation to avoid "Models aren't loaded yet" error
lazy_get_all_models = lazy(get_all_models, list)


class Method(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class MyModels(models.Model):
    model_name = models.CharField(max_length=255, choices=lazy_get_all_models(),unique = True)
    
    def __str__(self):
        return self.model_name

    
class ModelMethod(models.Model):
    method = models.ManyToManyField(Method, related_name="modelmethod")
    model_name = models.OneToOneField(MyModels,on_delete=models.CASCADE)

    def __str__(self):
        return self.model_name.model_name

