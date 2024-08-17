import flet as ft
import requests
import time

PREGAME_PAGE_TIME = 15
DISCUSSION_TIME = 10    # 120
VOTING_TIME = 30        # 25
WINNER_TIME = 15
CONTINUE_TIME = 10
VOTED_OUT_TIME = 5


def main(page: ft.Page):
    class User:
        def __init__(self, username='', lobby=None):
            self.username: str = username
            self.lobby: str | None = lobby
            self.ready: bool = False
            self.my_word: str | None = None
            self.user_type: str | None = None

    user = User()

    url = 'http://127.0.0.1:8001'
    page.title = "Deception"

    def confirm_username(player: User, u_name):
        player.username = u_name
        page.go("/lobby_choose")

    def route_change(route):
        username_entry = ft.TextField(value=user.username, text_align=ft.TextAlign.CENTER, width=400)
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
            src="./Play.png",
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

        lobby1_button = ft.Image(
            src="./lobbybut1.png",
            width=300,
            height=100,
            border_radius=ft.border_radius.all(10),
        )
        lobby2_button = ft.Image(
            src="./lobbybut2.png",
            width=300,
            height=100,
            border_radius=ft.border_radius.all(10),
        )
        lobby3_button = ft.Image(
            src="./lobbybut3.png",
            width=300,
            height=100,
            border_radius=ft.border_radius.all(10),
        )
        lobby4_button = ft.Image(
            src="./lobbybut4.png",
            width=300,
            height=100,
            border_radius=ft.border_radius.all(10),
        )

        wait_cat = ft.Image(
            src ="./waitcat.PNG",
            width=150,
            height=150,
            border_radius=ft.border_radius.all(10),
        )

        page.views.clear()

        if page.route == "/":
            page.theme_mode = ft.ThemeMode.LIGHT
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
                        # ft.ElevatedButton("tempbut", on_click=lambda _: page.go("/votedone"))
                    ],
                )
            )
            page.update()
        if page.route == "/lobby_choose":
            page.theme_mode = ft.ThemeMode.DARK

            def go_into_lobby(player: User, lob):
                player.lobby = lob
                can_join = requests.get(url + "/lobby_status?lobby=" + player.lobby).json()
                if can_join:
                    page.go("/waiting")
                back = requests.post(url + '/enter_lobby?lobby=' + player.lobby + "&player=" + player.username).json()

            button_container1 = ft.Container(height=300,
                                             alignment=ft.alignment.bottom_center,
                                             margin=0,
                                             content=ft.ElevatedButton(content=lobby1_button,
                                                                       on_click=lambda _: go_into_lobby(user,
                                                                                                        'lobby1')),
                                             )
            button_container2 = ft.Container(height=250,
                                             alignment=ft.alignment.center,
                                             margin=-75,
                                             content=ft.ElevatedButton(content=lobby2_button,
                                                                       on_click=lambda _: go_into_lobby(user, 'lobby2'))
                                             )
            button_container3 = ft.Container(height=250,
                                             alignment=ft.alignment.center,
                                             margin=-75,
                                             content=ft.ElevatedButton(content=lobby3_button,
                                                                       on_click=lambda _: go_into_lobby(user, 'lobby3'))
                                             )
            button_container4 = ft.Container(height=250,
                                             margin=-75,
                                             alignment=ft.alignment.center,
                                             content=ft.ElevatedButton(content=lobby4_button,
                                                                       on_click=lambda _: go_into_lobby(user, 'lobby4'))
                                             )
            button_container5 = ft.Container(height=30,
                                             margin=5,
                                             alignment=ft.alignment.center,
                                             content=ft.ElevatedButton("Go Home",
                                                                       on_click=lambda _: page.go('/'))
                                             )

            backgroundcontainer = ft.Container(
                alignment=ft.alignment.center,
                content=ft.Column(
                    [button_container1, button_container2, button_container3, button_container4,
                     button_container5]),

            )

            page.views.append(
                ft.View(
                    "/lobby_choose",
                    [
                        ft.Column([ft.Container(content=ft.Stack([
                            ft.Image(src='LobbyBackground.png',
                                     ),backgroundcontainer]))]),

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
                        ft.Text("Words: \
                    At the beginning of each round, a word is chosen.\
                    Liars: Receive 40-50% of the word.\
                    Players: Receive the full word."),
                        ft.Text("Gameplay:"),
                        ft.Text("Discussion Phase:"),
                        ft.Text("Duration: 2 minute.\
                    Players and Liars discuss their word without revealing the actual word or showing their screens.\
                    The goal is to identify inconsistencies in others' descriptions to detect the Liars."),
                        ft.Text("Voting Phase:"),
                        ft.Text("Duration:30 seconds.\
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
            def retrieve_word(player: User):
                word_req = requests.get(url + '/get_word?lobby=' + player.lobby + '&player=' + player.username).json()
                user.my_word = word_req

            def leave_lobby(player: User):
                player_list = requests.post(url + '/player_leave?lobby=' + player.lobby + "&player=" + player.username).json()
                player.lobby = None
                page.go('/lobby_choose')

            def ready_up(player: User, status):
                back = requests.post(url + '/ready_up?lobby=' + user.lobby + '&player=' + user.username).json()
                if player.username in back:
                    status.value = 'Ready to go!'
                    user.ready = True
                else:
                    status.value = "Not ready"
                    user.ready = False
                page.update()

            ready_status = ft.Text("Not ready")
            lobby_player_list = ft.Text('')

            page.views.append(
                ft.View(
                    "/waiting",
                    [
                        ft.Container(
                            content=wait_cat,
                            alignment=ft.alignment.center,
                        ),

                        ft.AppBar(title=ft.Text(f"Lobby {user.lobby[-1]}"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ready_status,
                        lobby_player_list,
                        ft.Container(
                            content=ft.ElevatedButton("Ready", on_click=lambda _: ready_up(user, ready_status)),
                            alignment=ft.alignment.center,
                        ),
                        ft.Container(
                            content=ft.ElevatedButton("Leave Lobby", on_click=lambda _: leave_lobby(user)),
                            alignment=ft.alignment.center,
                        ),
                    ]
                )
            )
            while True:
                time.sleep(1)
                player_list = requests.get(url + '/players?lobby=' + user.lobby).json()
                if user.ready:
                    retrieve_word(user)
                    if user.my_word:
                        if '_' in user.my_word:
                            user.user_type = 'liar'
                            page.go('/liar')
                            break
                        else:
                            user.user_type = 'player'
                            page.go('/player')
                            break
                lobby_player_list.value = '\n'.join(player_list)
                page.update()

        if page.route == "/liar":
            page.theme_mode = ft.ThemeMode.DARK
            pregame_time = ft.Text(value=f'{PREGAME_PAGE_TIME}', text_align=ft.TextAlign.CENTER, width=100)
            pregame_timer = ft.Container(height=500,
                                         alignment=ft.alignment.bottom_left,
                                         margin=0,
                                         content=pregame_time,
                                         )
            backgroundcontainer = ft.Container(
                alignment=ft.alignment.center,
                content=ft.Column(
                    [pregame_timer]),

            )
            page.views.append(
                ft.View(
                    "/liar",
                    [
                        ft.Column([ft.Container(content=ft.Stack([
                            ft.Image(src='liarpage.png',
                                     ), backgroundcontainer]))]),
                        ft.Text(value=f'The word is {user.my_word}')
                    ],
                )
            )
            page.update()
            general_timer(pregame_time, '/discussion')

        if page.route == "/player":
            page.theme_mode = ft.ThemeMode.LIGHT
            pregame_time = ft.Text(value=f'{PREGAME_PAGE_TIME}', text_align=ft.TextAlign.CENTER, width=100)
            pregame_timer = ft.Container(height=500,
                                         alignment=ft.alignment.bottom_left,
                                         margin=0,
                                         content=pregame_time,
                                         )
            backgroundcontainer = ft.Container(
                alignment=ft.alignment.center,
                content=ft.Column(
                    [pregame_timer]),

            )
            page.views.append(
                ft.View(
                    "/player",
                    [
                        ft.Column([ft.Container(content=ft.Stack([
                            ft.Image(src='playerpage.png',
                                     ), backgroundcontainer]))]),
                        ft.Text(value=f'The word is {user.my_word}')
                    ],
                )
            )
            page.update()
            general_timer(pregame_time, '/discussion')

        if page.route == "/discussion":
            page.theme_mode = ft.ThemeMode.DARK
            discussion_time = ft.Text(value=f'{DISCUSSION_TIME}', text_align=ft.TextAlign.CENTER,size=50, weight=ft.FontWeight.W_100, width=100)
            discusstimer = ft.Container(height=400,
                                        alignment=ft.alignment.bottom_center,
                                        margin=0,
                                        content=discussion_time,
                                        )
            backgroundcontainer = ft.Container(
                alignment=ft.alignment.center,
                content=ft.Column(
                    [discusstimer]),

            )
            page.views.append(
                ft.View(
                    "/discussion",
                    [
                        ft.Column([ft.Container(content=ft.Stack([
                            ft.Image(src='DiscussPage.png',
                                     ), backgroundcontainer]))])
                    ],
                )
            )
            general_timer(discussion_time, '/voting')
            page.update()
        if page.route == "/voting":
            vote_time = ft.Text(value=f'{VOTING_TIME}', text_align=ft.TextAlign.CENTER, width=100)

            def send_vote(voted_player):
                print(f'voted player inital: {voted_player}')
                voted_player = 'changed'
                print(f'{user.username} is voting out {voted_player}')
                ret = requests.post(url + '/send_vote?lobby=' + user.lobby + '&voted_player=' + voted_player).json()
                print('return after vote')
                print(ret)
                page.go('/votedone')

            view = ft.View(
                "/voting",
                [
                    ft.AppBar(title=ft.Text("Vote"), bgcolor=ft.colors.SURFACE_VARIANT),
                    vote_time,
                ],
            )

            players = requests.get(url + '/players?lobby=' + user.lobby).json() + requests.get(url + '/liar_list?lobby=' + user.lobby).json()

            players.remove(user.username)
            for player in players:
                view.controls.append(ft.ElevatedButton(text=players, on_click=lambda _: send_vote(voted_player=player)))
            page.views.append(view)
            page.update()
            general_timer(vote_time, '/votedone')

            if int(vote_time.value) <= 0:
                state: str = requests.get(url + '/get_game_state?lobby=' + user.lobby + '&player=' + user.username).json()
                if state == 'PLAYERWIN':
                    page.go('/playerwin')
                elif state == 'LIARWIN':
                    page.go('/liarwin')
                elif state == 'VOTEDOUT':
                    page.go('/votedout')
                elif state == 'CONTINUE':
                    page.go('/continue')
                else:
                    # something fucked up
                    page.go('/')



        if page.route == "/liarwin":
            status_time = ft.Text(value=f'{WINNER_TIME}', text_align=ft.TextAlign.CENTER, width=100)
            wintimer = ft.Container(height=400,
                                    alignment=ft.alignment.bottom_center,
                                    margin=0,
                                    content=status_time,
                                    )
            backgroundcontainer = ft.Container(
                alignment=ft.alignment.center,
                content=ft.Column(
                    [wintimer]))
            page.views.append(
                ft.View(
                    "/liarwin",
                    [
                        ft.Column([ft.Container(content=ft.Stack([
                            ft.Image(src='placeholder.png',
                                     ), backgroundcontainer]))])
                    ],
                )
            )
            general_timer(status_time, '/')
            page.update()
        if page.route == "/playerwin":
            status_time = ft.Text(value=f'{WINNER_TIME}', text_align=ft.TextAlign.CENTER, width=100)
            wintimer = ft.Container(height=400,
                                    alignment=ft.alignment.bottom_center,
                                    margin=0,
                                    content=status_time,
                                    )
            backgroundcontainer = ft.Container(
                alignment=ft.alignment.center,
                content=ft.Column(
                    [wintimer]))
            page.views.append(
                ft.View(
                    "/playerwin",
                    [
                        ft.Column([ft.Container(content=ft.Stack([
                            ft.Image(src='pwin.png',
                                     ), backgroundcontainer]))])
                    ],
                )
            )
            general_timer(status_time, '/')
            page.update()

        if page.route == "/votedone":

            page.views.append(
                ft.View(
                    "/votedone",
                    [
                        ft.Image(src="uhavevoted.PNG")
                    ],
                )
            )
            page.update()

        if page.route == "/continue":
            status_time = ft.Text(value=f'{CONTINUE_TIME}', text_align=ft.TextAlign.CENTER, width=100)
            page.views.append(
                ft.View(
                    "/continue",
                    [
                        ft.AppBar(title=ft.Text("The game continues"), bgcolor=ft.colors.SURFACE_VARIANT),
                        status_time,
                    ],
                )
            )

            ret = requests.get(url).json()
            if user.username in ret[user.lobby]['liars']:
                page_to_go = '/liar'
                user.my_word = requests.get(url + '/get_word?lobby=' + user.lobby + '&player=' + user.username).json()
            elif user.username in ret[user.lobby]['active_players']:
                page_to_go = '/player'
                user.my_word = requests.get(url + '/get_word?lobby=' + user.lobby + '&player=' + user.username).json()
            elif user.username in ret[user.lobby]['voted_out_players']:
                page_to_go = '/votedout'
            else:
                page_to_go = '/'
            general_timer(status_time, page_to_go)
            page.update()

        if page.route == "/votedout":
            #CHANGE THE TIME OF THIS
            status_time = ft.Text(value=f'{VOTED_OUT_TIME}', text_align=ft.TextAlign.CENTER, width=100)
            page.views.append(
                ft.View(
                    "/votedout",
                    [
                        ft.AppBar(title=ft.Text("you have been voted out"), bgcolor=ft.colors.SURFACE_VARIANT),
                        status_time,
                    ],
                )
            )
            page.update()
            reset_player(user)
            general_timer(status_time, '/')


    def reset_player(player: User):
        player.lobby = None
        player.my_word = None
        player.ready = False

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

    def general_timer(gtime, next_page):
        while int(gtime.value) > 0:
            time.sleep(1)
            gtime.value = int(gtime.value) - 1
            page.update()
        page.go(next_page)


ft.app(target=main, name='game',view=ft.AppView.WEB_BROWSER,assets_dir='assets')

# ft.app(target=main, name='game')


