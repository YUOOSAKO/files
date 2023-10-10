import unittest
import os
from tweets_data_collector import parse_search_category

class TestGetSearchCategory(unittest.TestCase):
    def test_search_category(self):
        file_path = "search_category/fortnite.json"
        self.assertTrue(os.path.isfile(file_path))
        designations, relates = parse_search_category(file_path)
        self.assertEqual(
            [
                "フォートナイト", 
                "フォトナ",
                "Fortnite"
            ], 
            designations
        )
        
        self.assertEqual(
            [
                "アップデート", 
                "アプデ",
                "update",
                "ダウンタイム",
                "downtime"
            ],
            relates
        )
        
if __name__ == "__main__":
    unittest.main()