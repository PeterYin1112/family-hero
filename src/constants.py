import pygame

# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Family Hero Quest"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
CYAN = (0, 255, 255)
PINK = (255, 105, 180)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)
DARK_GREY = (50, 50, 50)

# Characters
CHAR_DAUGHTER = "daughter"
CHAR_SON = "son"
CHAR_MOM = "mom"
CHAR_DAD = "dad"

CHAR_CONFIG = {
    CHAR_DAUGHTER: {
        "name": "Daughter",
        "display_name": "印品榕",
        "theme": "Ice Princess",
        "colors": (CYAN, PINK),
        "attack_style": "Ice Blast"
    },
    CHAR_SON: {
        "name": "Son",
        "display_name": "印晨希",
        "theme": "Beetle King",
        "colors": (GREEN, BLUE),
        "attack_style": "Beetle Charge"
    },
    CHAR_MOM: {
        "name": "Mom",
        "display_name": "印媽媽",
        "theme": "Wonder Woman",
        "colors": (YELLOW, RED),
        "attack_style": "Magic"
    },
    CHAR_DAD: {
        "name": "Dad",
        "display_name": "印爸爸",
        "theme": "Super Dad",
        "colors": (GREY, BLUE),
        "attack_style": "Power Punch"
    }
}

# Vocabulary Data
DEFAULT_VOCAB = {
    "animals": [
        {"en": "cat", "zh": "貓", "type": "noun"},
        {"en": "dog", "zh": "狗", "type": "noun"},
        {"en": "pig", "zh": "豬", "type": "noun"},
        {"en": "bird", "zh": "鳥", "type": "noun"},
        {"en": "duck", "zh": "鴨子", "type": "noun"},
        {"en": "lion", "zh": "獅子", "type": "noun"},
        {"en": "fish", "zh": "魚", "type": "noun"},
        {"en": "monkey", "zh": "猴子", "type": "noun"},
        {"en": "tiger", "zh": "老虎", "type": "noun"},
        {"en": "zebra", "zh": "斑馬", "type": "noun"}
    ],
    "food": [
        {"en": "apple", "zh": "蘋果", "type": "noun"},
        {"en": "banana", "zh": "香蕉", "type": "noun"},
        {"en": "egg", "zh": "蛋", "type": "noun"},
        {"en": "cake", "zh": "蛋糕", "type": "noun"},
        {"en": "milk", "zh": "牛奶", "type": "noun"},
        {"en": "water", "zh": "水", "type": "noun"},
        {"en": "rice", "zh": "米飯", "type": "noun"},
        {"en": "candy", "zh": "糖果", "type": "noun"}
    ],
    "nature": [
        {"en": "sun", "zh": "太陽", "type": "noun"},
        {"en": "moon", "zh": "月亮", "type": "noun"},
        {"en": "star", "zh": "星星", "type": "noun"},
        {"en": "tree", "zh": "樹", "type": "noun"},
        {"en": "flower", "zh": "花", "type": "noun"},
        {"en": "book", "zh": "書", "type": "noun"},
        {"en": "pen", "zh": "筆", "type": "noun"},
        {"en": "bag", "zh": "書包", "type": "noun"},
        {"en": "bus", "zh": "公車", "type": "noun"},
        {"en": "car", "zh": "車子", "type": "noun"}
    ],
    "body": [
        {"en": "eye", "zh": "眼睛", "type": "noun"},
        {"en": "nose", "zh": "鼻子", "type": "noun"},
        {"en": "mouth", "zh": "嘴巴", "type": "noun"},
        {"en": "hand", "zh": "手", "type": "noun"}
    ],
    "verbs": [
        {"en": "run", "zh": "跑", "type": "verb"},
        {"en": "jump", "zh": "跳", "type": "verb"},
        {"en": "walk", "zh": "走路", "type": "verb"},
        {"en": "swim", "zh": "游泳", "type": "verb"},
        {"en": "fly", "zh": "飛", "type": "verb"},
        {"en": "eat", "zh": "吃", "type": "verb"},
        {"en": "drink", "zh": "喝", "type": "verb"},
        {"en": "sleep", "zh": "睡覺", "type": "verb"},
        {"en": "draw", "zh": "畫畫", "type": "verb"},
        {"en": "sing", "zh": "唱歌", "type": "verb"}
    ],
    "adjectives": [
        {"en": "big", "zh": "大的", "type": "adj"},
        {"en": "small", "zh": "小的", "type": "adj"},
        {"en": "hot", "zh": "熱的", "type": "adj"},
        {"en": "cold", "zh": "冷的", "type": "adj"},
        {"en": "happy", "zh": "快樂的", "type": "adj"},
        {"en": "sad", "zh": "難過的", "type": "adj"},
        {"en": "red", "zh": "紅色的", "type": "adj"},
        {"en": "blue", "zh": "藍色的", "type": "adj"}
    ],
    "numbers": [
        {"en": "one", "zh": "一", "type": "noun"},
        {"en": "two", "zh": "二", "type": "noun"},
        {"en": "three", "zh": "三", "type": "noun"},
        {"en": "four", "zh": "四", "type": "noun"},
        {"en": "five", "zh": "五", "type": "noun"},
        {"en": "six", "zh": "六", "type": "noun"},
        {"en": "seven", "zh": "七", "type": "noun"},
        {"en": "eight", "zh": "八", "type": "noun"},
        {"en": "nine", "zh": "九", "type": "noun"},
        {"en": "ten", "zh": "十", "type": "noun"}
    ]
}

BROTHER_FOCUS_WORDS = [
    {"en": "tired", "zh": "累的", "type": "adj"},
    {"en": "angry", "zh": "生氣的", "type": "adj"},
    {"en": "strong", "zh": "強壯的", "type": "adj"},
    {"en": "thin", "zh": "瘦的", "type": "adj"},
    {"en": "short", "zh": "短/矮的", "type": "adj"},
    {"en": "tall", "zh": "高的", "type": "adj"}
]

# Paths
FONT_PATH = "assets/fonts/font.ttf"
SAVE_FILE = "save_data.json"
