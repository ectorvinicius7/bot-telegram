import unittest

from handlers.products import format_product, load_products


class ProductsTest(unittest.TestCase):
    def test_load_products_returns_four_examples(self):
        products = load_products()

        self.assertEqual(len(products), 4)
        self.assertTrue(all("name" in product for product in products))
        self.assertTrue(all("price" in product for product in products))
        self.assertTrue(all("description" in product for product in products))
        self.assertTrue(all("link" in product for product in products))

    def test_format_product_includes_details(self):
        product = load_products()[0]
        formatted = format_product(product)

        self.assertIn(product["name"], formatted)
        self.assertIn(product["price"], formatted)
        self.assertIn(product["description"], formatted)
        self.assertIn(product["link"], formatted)


if __name__ == "__main__":
    unittest.main()
