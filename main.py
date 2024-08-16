import flet as ft
import requests
import time

PREGAME_PAGE_TIME = 10


def main(page: ft.Page):
    class User:
        def __init__(self, username='', lobby=None):
            self.username: str = username
            self.lobby: str | None = lobby
            self.get_word: bool = False
            self.my_word: str | None = None

    user = User()
    page.theme_mode = ft.ThemeMode.LIGHT
    username: str = ''
    lobby: str | None = None

    url = 'http://127.0.0.1:8001'
    page.title = "Deception"

    def confirm_username(player: User, u_name):
        player.username = u_name
        page.go("/lobby_choose")

    def route_change(route):
        username_entry = ft.TextField(value='', text_align=ft.TextAlign.CENTER, width=400)
        title_image = ft.Image(
                            src ="./Title.png",
                            width=500,
                            height=200,
                            border_radius=ft.border_radius.all(10),
                        )

        home_cat = ft.Image(
                            src ="./HomeCat.jpg",
                            width=150,
                            height=150,
                            border_radius=ft.border_radius.all(10),
                        )

        play_button = ft.Image(
                            src ="./Play.png",
                            width=300,
                            height=100,
                            border_radius=ft.border_radius.all(10),
                        )

        rules_button = ft.Image(
                            src ="./Rules.png",
                            width=300,
                            height=100,
                            border_radius=ft.border_radius.all(10),
                        )

        page.views.clear()

        if page.route == "/":
            page.update()
            page.views.append(

                ft.View(
                    "/",

                    [ft.Container(
                        content=title_image,
                        alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=home_cat,
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=ft.Text("Username"),
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=username_entry,
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=ft.ElevatedButton(content=play_button, on_click=lambda _: confirm_username(user, username_entry.value)),
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=ft.ElevatedButton(content=rules_button, on_click=lambda _: page.go("/rules")),
                            alignment=ft.alignment.center,
                        ),
                    ],
                )
            )
        if page.route == "/lobby_choose":
            # background = ft.Container(
            #     image_src="LobbyBackground.png"
            # )
            #
            # button_container1 = ft.Container(
            #     alignment=ft.alignment.center,
            #     content=ft.ElevatedButton("Join Lobby 1", on_click=lambda _: go_into_lobby(user, 'lobby1')),
            # )
            #
            # backgroundcontainer = ft.Container(
            #     alignment=ft.alignment.center,
            #     content=ft.Stack([background,button_container1])
            # )
            def go_into_lobby(player: User, lobby):
                player.lobby = lobby
                can_join = requests.get(url + "/lobby_status?lobby=" + player.lobby).json()
                if can_join:
                    page.go("/waiting")
                back = requests.post(url + '/db?lobby=' + player.lobby + "&player=" + player.username).json()

            page.views.append(
                ft.View(
                    "/lobby_choose",
                    [
                        # ft.Column([ft.Container(content=ft.Stack([
                        #     ft.Image(src='LobbyBackground.png',
                        #              ),backgroundcontainer]))]),
                        ft.AppBar(title=ft.Text("Join a lobby"), bgcolor=ft.colors.SURFACE_VARIANT),

                        ft.ElevatedButton("Join Lobby 1", on_click=lambda _: go_into_lobby(user, 'lobby1')),
                        ft.ElevatedButton("Join Lobby 2", on_click=lambda _: go_into_lobby(user, 'lobby2')),
                        ft.ElevatedButton("Join Lobby 3", on_click=lambda _: go_into_lobby(user, 'lobby3')),
                        ft.ElevatedButton("Join Lobby 4", on_click=lambda _: go_into_lobby(user, 'lobby4')),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ]
                )
            )


            page.update()
        if page.route == "/rules":
            page.views.append(
                ft.View(
                    "/rules",
                    [
                        ft.AppBar(title=ft.Text("Rules"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Text("How To Play"),
                        ft.Text("Setup:"),
                        ft.Text("Objective: \
                    Liars: Successfully deceive the Players by lying about the word to avoid detection. \
                    Players: Identify and vote out all Liars before they equal or outnumber the Players."),
                        ft.Text("Roles: \
                    Liars: A certain number of players are randomly assigned as Liars. \
                    Players: The rest of the players are designated as Players."),
                        ft.Text("Words: \
                    At the beginning of each round, a word is chosen.\
                    Liars: Receive 10-20% of the word (minimum of 1 letter).\
                    Players: Receive the full word."),
                        ft.Text("Gameplay:"),
                        ft.Text("Discussion Phase:"),
                        ft.Text("Duration: 1 minute.\
                    Players and Liars discuss their word without revealing the actual word or showing their screens.\
                    The goal is to identify inconsistencies in others' descriptions to detect the Liars."),
                        ft.Text("Voting Phase:\
                    After the discussion, all players must vote on who they think the Liar(s) is/are.\
                    The player(s) with the most votes are revealed and removed from the game."),
                        ft.Text("End of Round:\
                    If all Liars are correctly identified and voted out, the game ends, and the Players win.\
                    If any Liars remain, the game continues to the next round with a new word."),
                        ft.Text("Win Conditions:"),
                        ft.Text("Players Win: If all Liars are identified and voted out before the number of Liars equals the number of Players.\
                    Liars Win: If the number of Liars becomes equal to or greater than the number of Players at any point in the game."),
                        ft.Text("Additional Rules:"),
                        ft.Text("In case of a tie during voting, a coin will be flipped and one player will be out.\
                    Players can only vote for a specific individual once per game."),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        if page.route == "/waiting":

            def retrieve_word(player):
                word_req = requests.get(url + '/get_word?lobby=' + player.lobby + '&player=' + player.username).json()
                user.my_word = word_req

            def leave_lobby(player: User):
                player_list = requests.post(url + '/player_leave?lobby=' + player.lobby + "&player=" + player.username)
                player.lobby = None
                page.go('/lobby_choose')

            def ready_up(player: User, status):
                back = requests.post(url + '/ready_up?lobby=' + user.lobby + '&player=' + user.username).json()
                # print(back)
                if player.username in back:
                    status.value = 'Ready to go!'
                    user.get_word = True
                else:
                    status.value = "Not ready"
                    user.get_word = False
                page.update()

            lobby_player_list = ft.Text('Lobby Player List Placeholder')
            ready_status = ft.Text("Not ready")

            page.views.append(
                ft.View(
                    "/waiting",
                    [
                        ft.AppBar(title=ft.Text(f"Lobby {user.lobby[-1]}"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ready_status,
                        lobby_player_list,
                        ft.ElevatedButton("Ready", on_click=lambda _: ready_up(user, ready_status)),
                        ft.ElevatedButton("Leave Lobby", on_click=lambda _: leave_lobby(user)),
                    ]
                )
            )
            while True:
                time.sleep(2)
                player_list = requests.get(url + '/players?lobby=' + user.lobby).json()
                if user.get_word:
                    retrieve_word(user)
                lobby_player_list.value = '\n'.join(player_list)
                page.update()

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
                        ft.AppBar(title=ft.Text("Discuss."), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Text("Who is the op?"),
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
        page.update()


    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    def general_timer(gtime):
        if int(gtime.value) == PREGAME_PAGE_TIME:
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

ft.app(target=main, name='game',view=ft.AppView.WEB_BROWSER,assets_dir='assets')

# ft.app(target=main, name='game')


