import fastapi
import uvicorn
import random

easy_word_list: list[str] = [
    "apple", "berry", "chair", "table", "grass", "beach", "cloud", "storm", "stone",
    "ocean", "river", "field", "plant", "bloom", "earth", "world", "peace", "water",
    "flame", "light", "night", "day", "sleep", "dream", "heart", "faith", "truth",
    "trust", "smile", "laugh", "tears", "voice", "sound", "music", "color", "shade",
    "black", "white", "green", "blue", "red", "yellow", "brown", "purple", "silver",
    "gold", "quiet", "noisy", "happy", "sad", "angry", "sorry", "alone", "calm",
    "crazy", "magic", "fancy", "quick", "ready", "early", "tired", "happy", "sleep",
    "apple", "banana", "grape", "mango", "melon", "peach", "plum", "lemon", "berry",
    "olive", "cherry", "apricot", "beetle", "insect", "spider", "bug", "crab",
    "shell", "clams", "waves", "algae", "kelp", "stone", "grass", "leaves", "moss",
    "woods", "river", "rocks", "trail", "path", "hills", "steps", "climb", "rocks",
    "rope", "cabin", "small", "large", "house", "rooms", "walls", "brick", "floor",
    "carpet", "sheets", "towel", "light", "lamp", "curtain", "mirror", "books", "piano",
    "vases", "photo", "clock", "timer", "radio", "phone", "cable", "tools", "tapes",
    "scarf", "boots", "shoes", "watch", "dress", "shirt", "pants", "belt", "jeans",
    "shorts", "glove", "beads", "rings", "chain", "clasp", "pouch", "purse", "shoes",
    "boots", "socks", "light", "lamp", "shade", "table", "books", "music", "paint",
    "brush", "paper", "photo", "frame", "paint", "mugs", "plate", "spoon", "fork",
    "glass", "drink", "flask", "knife", "chair", "stool", "bench", "sofa", "curtains",
    "broom", "mop", "trash", "bag", "bucket", "toilet", "basin", "towel", "tiles",
    "mirror", "tap", "door", "locks", "keys", "rooms", "walls", "paint", "brush",
    "chair", "stool", "bench", "table", "couch", "piano", "music", "stool", "clock",
    "radio", "phone", "alarm", "bell", "light", "bulb", "shade", "book", "table",
    "shelf", "wood", "nails", "tools", "paint", "rope", "board", "hinge", "wires",
    "glass", "bowl", "mugs", "plate", "knife", "glass", "pouch", "cans", "clock",
    "photo", "frame", "shoes", "pouch", "socks", "wires", "tools", "paint", "phone",
    "alarm", "bell", "light", "bulb", "photo", "frame", "mugs", "plate", "knife",
    "couch", "stool", "bench", "chair", "books", "photo", "frame", "glass", "plate",
    "knife", "paint", "brush", "phone", "alarm", "lamp", "shade", "table", "glass",
    "mugs", "frame", "phone", "alarm", "bell", "books", "music", "paint", "tools",
    "frame", "paint", "mugs", "plate", "glass", "plate", "clock", "photo", "frame",
    "table", "stool", "bench", "phone", "alarm", "bell", "light", "shade", "lamp"
]
hard_word_list: list[str] = [
    "garden", "flower", "window", "sunset", "morning", "spring", "summer", "winter",
    "autumn", "holiday", "travel", "journey", "explore", "discover", "nature", "animal",
    "forest", "desert", "island", "stream", "breeze", "thunder", "valley", "meadow",
    "sunrise", "horizon", "skyline", "village", "market", "cottage", "castle", "harbor",
    "lantern", "festival", "parade", "picnic", "orchard", "harvest", "sandwich", "blanket",
    "sunlight", "moonlight", "starlight", "glimmer", "sparkle", "whisper", "twilight",
    "daybreak", "midnight", "evening", "morning", "breakfast", "dinner", "supper", "lunch",
    "appetite", "kitchen", "stovetop", "bakery", "pastry", "dessert", "cookie", "brownie",
    "cupcake", "pancake", "waffle", "butter", "honey", "cereal", "oatmeal", "smoothie",
    "yogurt", "sundae", "iceberg", "volcano", "earth", "planet", "comet", "asteroid",
    "meteor", "galaxy", "nebula", "cosmos", "universe", "gravity", "orbit", "telescope",
    "eclipse", "sunbeam", "moonbeam", "starry", "cloudy", "rainbow", "thunderstorm",
    "lightning", "hurricane", "tornado", "blizzard", "snowfall", "snowflake", "hailstone",
    "puddle", "stream", "riverbank", "waterfall", "swamp", "lagoon", "coastline",
    "shoreline", "dockyard", "lighthouse", "seaside", "beachfront", "sandbar", "dolphin",
    "whale", "octopus", "seagull", "pelican", "albatross", "turtle", "lobster", "jellyfish",
    "starfish", "seaweed", "plankton", "seabed", "maritime", "sailor", "pirate", "treasure",
    "jungle", "savanna", "prairie", "wilderness", "campfire", "backpack", "trail", "compass",
    "binocular", "adventure", "quest", "odyssey", "voyage", "safari", "caravan", "highway",
    "avenue", "boulevard", "courtyard", "garden", "flower", "blossom", "sunflower",
    "orchid", "daffodil", "tulip", "daisy", "leaflet", "blossom", "thistle", "bamboo",
    "orchard", "gardener", "sandwich", "cookbook", "cottage", "greenhouse", "treehouse",
    "mountain", "waterfall", "village", "skyline", "horizon", "sunrise", "lantern",
    "fireplace", "cupboard", "bedroom", "kitchen", "laundry", "bathroom", "hallway",
    "library", "garage", "armchair", "wardrobe", "curtain", "carpet", "blanket", "pillow",
    "bedroom", "cabinet", "dresser", "cupboard", "staircase", "balcony", "sunshine",
    "sunlight", "daylight", "moonlight", "starlight", "lamplight", "skyline"
]


app = fastapi.FastAPI()

lobby_limit: int = 10

game_info = {
    'lobby1': {
        'in_game': False,
        'active_players': [],
        'voted_out_players': [],
        'liars': [],
        'current_word': '',
        'used_words': []
    },
    'lobby2': {
        'in_game': False,
        'active_players': [],
        'voted_out_players': [],
        'liars': [],
        'current_word': '',
        'used_words': []
    },
    'lobby3': {
        'in_game': False,
        'active_players': [],
        'voted_out_players': [],
        'liars': [],
        'current_word': '',
        'used_words': []
    },
    'lobby4': {
        'in_game': False,
        'active_players': [],
        'voted_out_players': [],
        'liars': [],
        'current_word': '',
        'used_words': []
    }
}


def hide_word(word: str, hide_perc=0.5) -> str:
    word = list(word)
    remove_lets = random.sample(word, k=int(len(list(word)) * hide_perc))
    for i, let in enumerate(list(word)):
        if let in remove_lets:
            word[i] = '_'
    return ' '.join(word)


@app.get('/')
def get_root():
    return game_info

@app.get('/players')
def get_players():
    return game_info['lobby1']['active_players']

@app.post('/db')
def add_player(item: str):
    game_info['lobby1']['active_players'].append(item)
    return game_info['lobby1']['active_players']


# uvicorn.run(app, host='127.0.0.1', port=8001)

if __name__ == '__main__':
    print(hide_word('courtyard', 0.5))
