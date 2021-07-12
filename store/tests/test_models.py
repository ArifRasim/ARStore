from django.test import TestCase

from store.models import Category, Product


class TestCategoriesModel(TestCase):
    def setUp(self):
        self.data1 = Category.objects.create(name='aaa', slug='aaa')

    def test_category_model_entry(self):
        """Test Category model data insertion/types/field attributes"""

        data = self.data1
        self.assertTrue(isinstance(data, Category))


# class TestProductsModel(TestCase):
#     def setUp(self):
#         self.data1 = Product.objects.create(title='atomic', category_id=1, created_by_id=1,
#                                             slug='atomic', price='20.20', image='django')
