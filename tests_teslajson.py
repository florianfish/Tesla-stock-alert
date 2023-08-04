import unittest
from unittest.mock import patch
from io import StringIO
from teslajson import process_model_data

class TestTeslaInventory(unittest.TestCase):

    def setUp(self):
        self.urls = {
            "MODEL Y": {
                'zipcode': "35000",
                'type': 'my',
                'url': "https://www.tesla.com/inventory/api/v1/inventory-results?query=%7B%22query%22%3A%7B%22model%22%3A%22my%22%2C%22condition%22%3A%22new%2C%22options%22%3A%7B%22TRIM%22%3A%5B%22MYRWD%22%5D%2C%22PAINT%22%3A%5B%22WHITE%22%2C%22BLUE%22%2C%22SILVER%22%5D%7D%2C%22arrangeby%22%3A%22Price%22%2C%22order%22%3A%22asc%22%2C%22market%22%3A%22FR%22%2C%22language%22%3A%22fr%22%2C%22super_region%22%3A%22north%20america%22%2C%22lng%22%3A-1.7075198%2C%22lat%22%3A48.11734209999999%2C%22zip%22%3A%2235000%22%2C%22range%22%3A50%2C%22region%22%3A%22FR%22%7D%2C%22offset%22%3A0%2C%22count%22%3A50%2C%22outsideOffset%22%3A0%2C%22outsideSearch%22%3Afalse%7D",
            },
            "MODEL 3": {
                'zipcode': "35000",
                'type': 'm3',
                'url': 'https://www.tesla.com/inventory/api/v1/inventory-results?query=%7B%22query%22%3A%7B%22model%22%3A%22m3%22%2C%22condition%22%3A%22new%22%2C%22options%22%3A%7B%22TRIM%22%3A%5B%22LRRWD%22%2C%22M3RWD%22%5D%2C%22PAINT%22%3A%5B%22GRAY%22%2C%22WHITE%22%2C%22BLUE%22%5D%7D%2C%22arrangeby%22%3A%22Price%22%2C%22order%22%3A%22asc%22%2C%22market%22%3A%22FR%22%2C%22language%22%3A%22fr%22%2C%22super_region%22%3A%22north%20america%22%2C%22lng%22%3A-1.7075198%2C%22lat%22%3A48.11734209999999%2C%22zip%22%3A%2244000%22%2C%22range%22%3A50%2C%22region%22%3A%22FR%22%7D%2C%22offset%22%3A0%2C%22count%22%3A50%2C%22outsideOffset%22%3A0%2C%22outsideSearch%22%3Afalse%7D',
            }
        }

    def test_process_model_data_with_valid_data(self):
        with patch("sys.stdout", new=StringIO()) as output:
            process_model_data("MODEL Y", "35000", "my", self.urls["MODEL Y"]["url"], True)
            process_model_data("MODEL 3", "35000", "m3", self.urls["MODEL 3"]["url"], False)
            output_str = output.getvalue()
            self.assertIn("MODEL Y", output_str)
            self.assertIn("MODEL 3", output_str)
            self.assertNotIn("Aucun résultats", output_str)

    def test_process_model_data_with_invalid_data(self):
        with patch("sys.stdout", new=StringIO()) as output:
            process_model_data("INVALID MODEL", "35000", "invalid_type", "invalid_url", True)
            output_str = output.getvalue()
            self.assertIn("Error!", output_str)

if __name__ == "__main__":
    unittest.main()
