# Scenario classes are imported here so locustfile.py stays clean.
# To register a new scenario: add its import below — nothing else changes.

from load_tests.scenarios.category_search import CategorySearchUser  # noqa: F401
from load_tests.scenarios.product_search import ProductSearchUser    # noqa: F401
