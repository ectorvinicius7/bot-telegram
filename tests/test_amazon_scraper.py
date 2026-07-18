import unittest

from amazon_scraper import _deduplicate_deals


class AmazonScraperTests(unittest.TestCase):
    def test_deduplicate_deals_by_link(self):
        deals = [
            {"title": "Produto A", "link": "https://example.com/p1"},
            {"title": "Produto A", "link": "https://example.com/p1"},
            {"title": "Produto B", "link": "https://example.com/p2"},
        ]

        result = _deduplicate_deals(deals)

        self.assertEqual(len(result), 2)
        self.assertEqual([item["link"] for item in result], ["https://example.com/p1", "https://example.com/p2"])


if __name__ == "__main__":
    unittest.main()
