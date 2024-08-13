import flet as ft
import requests
import time


url = 'http://127.0.0.1:8000'



def main(page: ft.Page):

    page.title = "Routes Example"

    number = ft.TextField(value='0', text_align=ft.TextAlign.CENTER, width=80)
    timer = ft.Text(value='300', text_align=ft.TextAlign.CENTER, width=50)
    req_field = ft.TextField(value='Nothing yet', text_align=ft.TextAlign.CENTER, width=400)
    add_field = ft.TextField(value='Add player here', text_align=ft.TextAlign.CENTER, width=400)

    def get_def():
        ret = requests.get(url)
        req_field.value = str(ret.json())
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
                    ft.ElevatedButton("Visit Store", on_click=lambda _: page.go("/store")),
                    ft.ElevatedButton("get general", on_click=lambda _: get_def()),
                    ft.ElevatedButton("get request", on_click=lambda _: get_players()),
                    ft.ElevatedButton("add player", on_click=lambda _: add_player(add_field.value)),
                    req_field,
                    add_field,
                    timer,
                ],
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
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    while int(timer.value) > 0:
        time.sleep(1)
        timer.value = int(timer.value) - 1
        page.update()


ft.app(target=main, name='game')


