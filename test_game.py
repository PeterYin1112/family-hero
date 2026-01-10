import unittest
import os
from src.constants import DEFAULT_VOCAB, CHAR_DAUGHTER, CHAR_SON
from src.data_manager import DataManager
from src.engines.math_engine import MathEngine
from src.engines.english_engine import EnglishEngine

class TestGameLogic(unittest.TestCase):
    def setUp(self):
        # Remove save file for clean slate
        if os.path.exists("save_data.json"):
            os.remove("save_data.json")
        self.dm = DataManager()
        self.math_engine = MathEngine(self.dm)
        self.english_engine = EnglishEngine(self.dm)

    def test_data_manager_defaults(self):
        data = self.dm.data
        self.assertIn("characters", data)
        self.assertIn(CHAR_DAUGHTER, data["characters"])
        self.assertIn("settings", data)
        self.assertEqual(data["settings"]["math_ranges"]["daughter"]["max"], 20)

    def test_math_engine(self):
        # Test Daughter simple addition
        q, a = self.math_engine.generate_question(CHAR_DAUGHTER)
        self.assertTrue("+" in q or "-" in q)
        self.assertTrue(int(a) >= 0)

        # Test Son advanced math (weights default to include others, but let's just check format)
        q, a = self.math_engine.generate_question(CHAR_SON)
        self.assertIsNotNone(q)
        self.assertIsNotNone(a)

    def test_english_engine(self):
        q_data = self.english_engine.generate_question(CHAR_SON)
        self.assertIsNotNone(q_data)
        self.assertIn("sentence", q_data)
        self.assertIn("answer", q_data)
        self.assertIn("context_zh", q_data)

    def tearDown(self):
        if os.path.exists("save_data.json"):
            os.remove("save_data.json")

if __name__ == '__main__':
    unittest.main()
