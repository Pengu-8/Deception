import flet as ft
import requests
import time

def main(page: ft.Page):

    url = 'http://127.0.0.1:8001'
    page.title = "test App"

    number = ft.TextField(value='0', text_align=ft.TextAlign.CENTER, width=80)
    timer = ft.Text(value='300', text_align=ft.TextAlign.CENTER, width=50)
    req_field = ft.TextField(value='Nothing yet', text_align=ft.TextAlign.CENTER, width=400)
    add_field = ft.TextField(value='Add player here', text_align=ft.TextAlign.CENTER, width=400)
    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def get_def():
        ret = requests.get(url)
        req_field.value = str(ret.json())
        page.update()

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    def get_players():
        ret = requests.get(url + '/players', )
        req_field.value = str(ret.json())
        page.update()

    def add_player(player):
        requests.post(url + '/db?item=' + player)
        get_players()

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Flet app"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.ElevatedButton("Play", on_click=lambda _: page.go("/lobby")),
                    ft.ElevatedButton("Visit Store", on_click=lambda _: page.go("/store")),
                    ft.ElevatedButton("add player", on_click=lambda _: add_player(add_field.value)),
                    req_field,
                    add_field,
                    timer,
                ],
            )
        )
        if page.route == "/lobby":
            page.views.append(
                ft.View(
                    "/lobby",
                    [
                        ft.AppBar(title=ft.Text("Lobby"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Join Lobby", on_click=lambda _: page.go("/waiting")),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ]
                )
            )
        if page.route == "/store":
            page.views.append(
                ft.View(
                    "/store",
                    [
                        ft.AppBar(title=ft.Text("Store"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        if page.route == "/waiting":
            page.views.append(
                ft.View(
                    "/waiting",
                    [
                        ft.AppBar(title=ft.Text("Waiting Area"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Start as Liar", on_click=lambda _: page.go("/liar")),
                        ft.ElevatedButton("Start as Player", on_click=lambda _: page.go("/player")),
                        ft.ElevatedButton("Leave Lobby", on_click=lambda _: page.go("/lobby")),
                        ft.Text(value=f"{lobby_list()}", text_align=ft.TextAlign.CENTER, width=100)
                    ],
                )
            )
        if page.route == "/liar":
            pregame_time = ft.Text(value='11', text_align=ft.TextAlign.CENTER, width=100)
            page.views.append(
                ft.View(
                    "/liar",
                    [
                        ft.AppBar(title=ft.Text("You are the ops (liar)"), bgcolor=ft.colors.SURFACE_VARIANT),
                        pregame_time,
                    ],
                )
            )
            general_timer(pregame_time)
        if page.route == "/player":
            pregame_time = ft.Text(value='11', text_align=ft.TextAlign.CENTER, width=100)
            page.views.append(
                ft.View(
                    "/player",
                    [
                        ft.AppBar(title=ft.Text("You are a real one (not liar)"), bgcolor=ft.colors.SURFACE_VARIANT),
                        pregame_time,
                    ],
                )
            )
            general_timer(pregame_time)
        if page.route == "/discussion":
            discussion_time = ft.Text(value='3', text_align=ft.TextAlign.CENTER, width=100)
            page.views.append(
                ft.View(
                    "/discussion",
                    [
                        ft.AppBar(title=ft.Text("Discuss, who is the op?"), bgcolor=ft.colors.SURFACE_VARIANT),
                        discussion_time,
                    ],
                )
            )
            general_timer(discussion_time)
        if page.route == "/voting":
            vote_time = ft.Text(value='6', text_align=ft.TextAlign.CENTER, width=100)
            page.views.append(
                ft.View(
                    "/voting",
                    [
                        ft.AppBar(title=ft.Text("Vote"), bgcolor=ft.colors.SURFACE_VARIANT),
                        vote_time,
                    ],
                )
            )
            general_timer(vote_time)
        if page.route == "/liarwin":
            status_time = ft.Text(value='20', text_align=ft.TextAlign.CENTER, width=100)
            page.views.append(
                ft.View(
                    "/liarwin",
                    [
                        ft.AppBar(title=ft.Text("Liar Wins"), bgcolor=ft.colors.SURFACE_VARIANT),
                        status_time,
                    ],
                )
            )
            general_timer(status_time)
        if page.route == "/playerwin":
            status_time = ft.Text(value='20', text_align=ft.TextAlign.CENTER, width=100)
            page.views.append(
                ft.View(
                    "/playerwin",
                    [
                        ft.AppBar(title=ft.Text("Players Win"), bgcolor=ft.colors.SURFACE_VARIANT),
                        status_time,
                    ],
                )
            )
            general_timer(status_time)
        if page.route == "/liaringame":
            status_time = ft.Text(value='20', text_align=ft.TextAlign.CENTER, width=100)
            page.views.append(
                ft.View(
                    "/liaringame",
                    [
                        ft.AppBar(title=ft.Text("Liar is still in the game."), bgcolor=ft.colors.SURFACE_VARIANT),
                        status_time,
                    ],
                )
            )
            general_timer(status_time)
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    def general_timer(gtime):
        if int(gtime.value) == 11:
            while int(gtime.value) > 0:
                time.sleep(1)
                gtime.value = int(gtime.value) - 1
                page.update()
            page.go("/discussion")
        elif int(gtime.value) == 3:
            while int(gtime.value) > 0:
                time.sleep(1)
                gtime.value = int(gtime.value) - 1
                page.update()
            page.go("/voting")
        elif int(gtime.value) == 6:
            while int(gtime.value) > 0:
                time.sleep(1)
                gtime.value = int(gtime.value) - 1
                page.update()
            page.go("/store")

    def lobby_list():
        response = requests.get(f"{url}/players")
        players = response.json()
        list_of_players = ""
        for player in players:
            list_of_players += f"{player}\n"
        return list_of_players


ft.app(target=main, name='game')


