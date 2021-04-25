from django.test import TestCase

from apps.tests import load_fixtures


class TestContributions(TestCase):
    fixtures = load_fixtures.load_fixtures()

    def test_regular(self):
        pass

    def test_regular_below_min(self):
        pass

    def test_regular_above_max(self):
        pass

    def test_y30(self):
        pass
