from demo.models import City, Country
from report_builder.registry import register


def register_test_catalogs():
    for model in [City, Country]:
        register(model)
