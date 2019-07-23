from django.contrib import admin
from demo.models import ProjectTest
# Register your models here.
from demo.catalogs import register_test_catalogs
# Register test catalogs
register_test_catalogs()
admin.site.register(ProjectTest)
