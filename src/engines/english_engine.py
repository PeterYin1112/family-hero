import random
from src.constants import CHAR_SON

class EnglishEngine:
    def __init__(self, data_manager):
        self.dm = data_manager

    def generate_question(self, char_id):
        settings = self.dm.get_settings()
        vocab_dict = settings["vocab"]

        # Collect all words
        all_words = []
        for category, words in vocab_dict.items():
            if category == "brother_focus":
                # Only add if character is Son, or maybe always mix them in with higher weight?
                # Prompt says: "Brother's Exclusive Focus Words (High Priority)"
                # I'll add them to the pool if it's the Son, or add them to general pool?
                # "Brother's Exclusive Focus Words" implies only he gets them OR he gets them more often.
                # "Shared Vocabulary (Base)" implies everyone gets those.
                continue
            all_words.extend(words)

        # If Son, add focus words
        if char_id == CHAR_SON:
            focus_words = vocab_dict.get("brother_focus", [])
            # Add them multiple times to increase probability?
            # Or just append them.
            all_words.extend(focus_words)
            # To make them "High Priority", let's add them again to weight them up
            all_words.extend(focus_words)

        # Pick a random word
        if not all_words:
            return None

        word_data = random.choice(all_words)
        return self._create_sentence(word_data)

    def _create_sentence(self, word_data):
        english_word = word_data["en"]
        chinese_meaning = word_data["zh"]
        w_type = word_data["type"]

        # Generate a simple sentence frame based on type
        # Ideally we'd have pre-written sentences, but for now we use templates.

        sentence = ""
        translation_context = ""

        if w_type == "noun":
            templates = [
                ("This is a ___.", "這是一個___。"),
                ("I see a ___.", "我看見一個___。"),
                ("The ___ is here.", "___在這裡。")
            ]
            tmpl = random.choice(templates)
            sentence = tmpl[0]
            translation_context = tmpl[1] # Shows "這是一個___。" so they know the context.

        elif w_type == "verb":
            templates = [
                ("I like to ___.", "我喜歡___。"),
                ("Can you ___?", "你會___嗎？"),
                ("Let's ___.", "我們一起___吧。")
            ]
            tmpl = random.choice(templates)
            sentence = tmpl[0]
            translation_context = tmpl[1]

        elif w_type == "adj":
            templates = [
                ("It is ___.", "它是___。"),
                ("I am ___.", "我很___。"),
                ("The car is ___.", "這輛車是___。")
            ]
            tmpl = random.choice(templates)
            sentence = tmpl[0]
            translation_context = tmpl[1]

        else:
            # Fallback
            sentence = f"Type the word: ___"
            translation_context = f"輸入單字: {chinese_meaning}"

        return {
            "sentence": sentence,
            "answer": english_word,
            "context_zh": translation_context, # The hint
            "meaning_zh": chinese_meaning # The word's meaning (maybe for result screen)
        }

    def get_options(self, correct_word, char_id):
        # Get 3 distractors
        settings = self.dm.get_settings()
        vocab_dict = settings["vocab"]
        all_words = []
        for category, words in vocab_dict.items():
             all_words.extend([w["en"] for w in words])

        # Remove correct word
        distractors = [w for w in all_words if w != correct_word]
        if len(distractors) < 3:
            random_distractors = distractors
        else:
            random_distractors = random.sample(distractors, 3)

        options = random_distractors + [correct_word]
        random.shuffle(options)
        return options
