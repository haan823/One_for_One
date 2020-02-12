from import_export import resources
from .models import Crawling


class CrawlingResource(resources.ModelResource):
    class Meta:
        model = Crawling