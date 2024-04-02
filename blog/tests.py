from django.test import TestCase

from blog.models import Category


# Create your tests here.
class TestCategory(TestCase):
    def test_delete_category(self):
        category = Category.objects.create(name="test")
        category.delete()
        self.assertEqual(Category.objects.count(), 0)
