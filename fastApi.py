import fastapi
import uvicorn
import random
import threading

# Yeah I know. I've had a long week cut me some slack
word_list: list[str] = [
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
    "jungle","olive", "cherry", "apricot", "beetle", "insect", "spider", "bug", "crab",
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
    "broom", "mop", "trash", "bag", "bucket", "toilet", "basin", "towel", "blossom", "thistle", "bamboo",
    "orchard", "gardener", "sandwich", "cookbook", "cottage", "greenhouse", "treehouse",
    "mountain", "waterfall", "village", "skyline", "horizon", "sunrise", "lantern",
    "fireplace", "cupboard", "bedroom", "kitchen", "laundry", "bathroom", "hallway",
    "library", "garage", "armchair", "wardrobe", "curtain", "carpet", "blanket", "pillow",
    "bedroom", "cabinet", "dresser", "cupboard", "staircase", "balcony", "sunshine",
    "sunlight", "daylight", "moonlight", "starlight", "lamplight", "skyline"
]


app = fastapi.FastAPI()

LOBBY_MAXIMUM: int = 4
LOBBY_MINIMUM: int = 3

game_info = {
    'lobby1': {
        'can_join': True,
        'players_ready': [],
        'active_players': [],
        'voted_out_players': [],
        'vote_count': [],
        'liars': [],
        'current_word': '',
        'used_words': []
    },
    'lobby2': {
        'can_join': True,
        'players_ready': [],
        'active_players': [],
        'voted_out_players': [],
        'vote_count': [],
        'liars': [],
        'current_word': '',
        'used_words': []
    },
    'lobby3': {
        'can_join': True,
        'players_ready': [],
        'active_players': [],
        'voted_out_players': [],
        'vote_count': [],
        'liars': [],
        'current_word': '',
        'used_words': []
    },
    'lobby4': {
        'can_join': True,
        'players_ready': [],
        'active_players': [],
        'voted_out_players': [],
        'vote_count': [],
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


def init_game(lobby: str):
    players: list[str] = game_info[lobby]['active_players']
    liar = random.sample(players, k=1)[0]
    game_info[lobby]['liars'].append(liar)
    game_info[lobby]['active_players'].remove(liar)
    new_round(lobby)


# get new word for next round
def new_round(lobby: str):
    game_info[lobby]['voted_out_players'].clear()
    while True:
        check_word = random.sample(word_list, k=1)[0]
        if check_word not in game_info[lobby]['used_words']:
            game_info[lobby]['current_word'] = check_word
            game_info[lobby]['used_words'].append(check_word)
            break

lock = threading.Lock()

@app.get('/')
def get_root():
    return game_info


@app.get('/lobby_status')
def get_lobby_status(lobby: str):
    return game_info[lobby]['can_join']


@app.get('/players')
def get_players(lobby: str):
    return game_info[lobby]['active_players']


@app.get('/liar_list')
def get_liars(lobby: str):
    return game_info[lobby]['liars']


@app.get('/get_word')
def get_word(lobby: str, player: str):
    word = game_info[lobby]['current_word']
    if player in game_info[lobby]['active_players']:
        return word
    return hide_word(word)


@app.get('/get_game_state')
def check_winner(lobby: str):
    with lock:
        if len(game_info[lobby]['vote_count']):
            count = {}
            for player in game_info[lobby]['vote_count']:
                if player in count:
                    count[player] += 1
                else:
                    count[player] = 1

            voted_out = max(count.items(), key=lambda x: x[1])[0]
            game_info[lobby]['voted_out_players'].append(voted_out)
            if voted_out in game_info[lobby]['active_players']:
                game_info[lobby]['active_players'].remove(voted_out)
            elif voted_out in game_info[lobby]['liars']:
                game_info[lobby]['liars'].remove(voted_out)

            new_round(lobby)

        if not len(game_info[lobby]['liars']):
            return 'PLAYERWIN'
        elif len(game_info[lobby]['active_players']) <= len(game_info[lobby]['liars']):
            return 'LIARWIN'
        return 'CONTINUE'


@app.post('/send_vote')
def vote_send(lobby: str, voted_player: str):
    with lock:
        game_info[lobby]['vote_count'].append(voted_player)
        return game_info[lobby]['vote_count']


@app.post('/reset_vote')
def reset(lobby: str):
    game_info[lobby]['vote_count'] = []
    return game_info[lobby]['vote_count']


@app.post('/enter_lobby')
def add_player(lobby: str, player: str):
    if player not in game_info[lobby]['active_players']:
        game_info[lobby]['active_players'].append(player)
    return game_info[lobby]['active_players']


@app.post('/reset_lobby')
def reset(lobby):
    game_info[lobby] = {
        'can_join': True,
        'players_ready': [],
        'active_players': [],
        'voted_out_players': [],
        'vote_count': [],
        'liars': [],
        'current_word': '',
        'used_words': []
    }
    return game_info[lobby]


@app.post('/player_leave')
def remove_player(lobby: str, player: str):
    while player in game_info[lobby]['active_players']:
        game_info[lobby]['active_players'].remove(player)
    return game_info[lobby]['active_players']


@app.post('/ready_up')
def toggle_ready(lobby: str, player: str):
    if player in game_info[lobby]['players_ready']:
        game_info[lobby]['players_ready'].remove(player)
    else:
        game_info[lobby]['players_ready'].append(player)

    if len(game_info[lobby]['players_ready']) == len(game_info[lobby]['active_players']) \
            and LOBBY_MINIMUM <= len(game_info[lobby]['active_players']) <= LOBBY_MAXIMUM:
        game_info[lobby]['can_join'] = False
        init_game(lobby)
    return game_info[lobby]['players_ready']


uvicorn.run(app, host='127.0.0.1', port=8001)

if __name__ == '__main__':
    print(hide_word('courtyard', 0.5))
