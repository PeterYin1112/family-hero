import json
import os
from src.constants import SAVE_FILE, DEFAULT_VOCAB, BROTHER_FOCUS_WORDS, CHAR_CONFIG

class DataManager:
    def __init__(self):
        self.data = self.load_data()

    def load_data(self):
        if not os.path.exists(SAVE_FILE):
            return self.create_default_data()

        try:
            with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return self.create_default_data()

    def create_default_data(self):
        # Combine default vocab with brother's focus words
        vocab = DEFAULT_VOCAB.copy()
        vocab["brother_focus"] = BROTHER_FOCUS_WORDS

        data = {
            "characters": {
                char_id: {"level": 1, "exp": 0, "equipment": [], "score": 0}
                for char_id in CHAR_CONFIG
            },
            "settings": {
                "math_weights": {
                    "daughter": {"add": 50, "sub": 50},
                    "son_dad": {"add_2d": 20, "sub_2d": 20, "add_3d": 10, "sub_3d": 10, "mult_2x1": 20, "mult_2x2": 10, "div": 10}
                },
                "math_ranges": {
                    "daughter": {"max": 20}
                },
                "vocab": vocab
            }
        }
        self.save_data(data)
        return data

    def save_data(self, data=None):
        if data:
            self.data = data
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def get_character_data(self, char_id):
        return self.data["characters"].get(char_id, {})

    def update_character_data(self, char_id, key, value):
        if char_id in self.data["characters"]:
            self.data["characters"][char_id][key] = value
            self.save_data()

    def get_settings(self):
        return self.data["settings"]

    def update_settings(self, category, key, value):
        if category in self.data["settings"]:
            self.data["settings"][category][key] = value
            self.save_data()
