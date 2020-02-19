from django.test import TestCase
from core.models import *

posting = Posting.objects.first()

posting.tag.filter(content='야식')
