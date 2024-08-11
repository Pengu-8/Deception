from fastapi import FastAPI
import uvicorn

player_list: list[str] = []

app = FastAPI()

@app.get('/')
def get_root():
    return {'home': 'page'}

@app.get('/players')
def get_players():
    return player_list

@app.post('/db')
def add_player(player):
    player_list.append(player)

uvicorn.run(app, host='127.0.0.1', port=8000)

