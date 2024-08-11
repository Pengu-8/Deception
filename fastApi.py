from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

game_info = {
    'player': []
}


@app.get('/')
def get_root():
    return game_info

@app.get('/players')
def get_players():
    return game_info['player']

@app.post('/db')
def add_player(item: str):
    game_info['player'].append(item)
    return game_info['player']

uvicorn.run(app, host='127.0.0.1', port=8000)

