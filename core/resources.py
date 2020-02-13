from import_export import resources
from .models import Store

class StoreResource(resources.ModelResource):
    class Meta:
        model = Store