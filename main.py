import flet as ft
import requests

url = 'http://127.0.0.1:8000'


def main(page: ft.Page):
    page.title = "Routes Example"

    # number = ft.TextField(value='0', text_align=ft.TextAlign.CENTER, width=80)

    req_field = ft.TextField(value='Nothing yet', text_align=ft.TextAlign.CENTER, width=400)
    add_field = ft.TextField(value='Add player here', text_align=ft.TextAlign.CENTER, width=400)

    def get_players():
        ret = requests.get(url + '/players')
        req_field.value = str(ret.content)
        page.update()

    def add_player():
        bruh = requests.post(url)

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Flet app"), bgcolor=ft.colors.SURFACE_VARIANT),
                    # ft.ElevatedButton("Visit Store", on_click=lambda _: page.go("/store")),
                    ft.ElevatedButton("get request", on_click=lambda _: get_players()),
                    ft.ElevatedButton("add player", on_click=lambda _: add_player()),
                    req_field,
                    add_field,
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


ft.app(target=main)