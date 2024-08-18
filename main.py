import flet as ft
import requests
import time

PREGAME_PAGE_TIME = 15
DISCUSSION_TIME = 120    # 120
VOTING_TIME = 20
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

    user = User()

    URL = 'http://127.0.0.1:8001'
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

        waitstart = ft.Image(
            src = "./waitstart.png",
            width=300,
            height=100,
            border_radius=ft.border_radius.all(10),
        )

        page.views.clear()

        if page.route == "/":
            page.theme_mode = ft.ThemeMode.LIGHT
            usertext = ft.Container(
                            content=ft.Text("Username"),
                            alignment=ft.alignment.center,
            )
            userent = ft.Container(
                            content=username_entry,
                            alignment=ft.alignment.center,
            )
            playbut = ft.Container(
                            content=ft.ElevatedButton(content=play_button, on_click=lambda _: confirm_username(user, username_entry.value)),
                            alignment=ft.alignment.center,
            )
            rulesbut = ft.Container(
                            content=ft.ElevatedButton(content=rules_button, on_click=lambda _: page.go("/rules")),
                            alignment=ft.alignment.center,
            )
            space = ft.Container(height=300, content=ft.Text(""))
            backgroundcontainer = ft.Container(
                alignment=ft.alignment.center,
                content=ft.Column(
                    [space,usertext, userent, playbut, rulesbut]))

            page.views.append(
                ft.View(
                    "/",

                    [
                        ft.Column([ft.Container(content=ft.Stack([
                            ft.Image(src='Homepage.png',
                                     ), backgroundcontainer]))])
                    ],
                )
            )
            page.update()
        if page.route == "/lobby_choose":
            page.theme_mode = ft.ThemeMode.DARK

            def go_into_lobby(player: User, lob):
                player.lobby = lob
                can_join = requests.get(URL + "/lobby_status?lobby=" + player.lobby).json()
                if can_join:
                    page.go("/waiting")
                back = requests.post(URL + '/enter_lobby?lobby=' + player.lobby + "&player=" + player.username).json()

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
            page.theme_mode = ft.ThemeMode.DARK
            rule1 = ft.Container(
                 alignment=ft.alignment.center,
                 margin=0,
                 content=ft.Text("  1. At the beginning of each round, each player receives a word.",size=15))
            rule2 = ft.Container(
                 alignment=ft.alignment.center,
                 margin=0,
                 content=ft.Text("  2. Liars receive a part of the word.",size=15))
            rule3 = ft.Container(
                alignment=ft.alignment.center,
                margin=0,
                content=ft.Text("   3. All players will discuss who they think is/are the Liar(s) without revealing the actual word.", size=15))
            rule4 = ft.Container(
                alignment=ft.alignment.center,
                margin=0,
                content=ft.Text("   4. If all Liars are voted out, the game ends, and the Players win.", size=15))
            rule5 = ft.Container(
                alignment=ft.alignment.center,
                margin=0,
                content=ft.Text("   5. If any Liars remain, the game continues to the next round with a new word.", size=15))
            rule6 = ft.Container(
                alignment=ft.alignment.center,
                margin=0,
                content=ft.Text("   6. If the number of Liars is equal to the number of Players, the Liars win.", size=15))
            homebut = ft.Container(
                alignment=ft.alignment.center,
                margin=0,
                content=ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")))
            space = ft.Container(ft.Text("", height=200))
            buttoncontainer = ft.Container(
                alignment=ft.alignment.bottom_center,
                content=ft.Column(
                    [space, rule1, rule2, rule3,rule4, rule5, rule6,homebut]),
            )

            page.views.append(
                ft.View(
                    "/rules",
                    [
                        ft.Column([ft.Container(content=ft.Stack([
                            ft.Image(src='RulesPage.PNG',
                                     ), buttoncontainer]))]),

                        # ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        if page.route == "/waiting":
            def retrieve_word(player: User):
                word_req = requests.get(URL + '/get_word?lobby=' + player.lobby + '&player=' + player.username).json()
                user.my_word = word_req

            def leave_lobby(player: User):
                player_list = requests.post(URL + '/player_leave?lobby=' + player.lobby + "&player=" + player.username).json()
                player.lobby = None
                page.go('/lobby_choose')

            def ready_up(player: User, status):
                back = requests.post(URL + '/ready_up?lobby=' + user.lobby + '&player=' + user.username).json()
                if player.username in back:
                    status.value = 'Ready to go!'
                    user.ready = True
                else:
                    status.value = "Not ready"
                    user.ready = False
                page.update()

            ready_status = ft.Text("Not ready",size=20)
            ready_status_container = ft.Container(alignment=ft.alignment.center, content=ready_status)
            playertext = ft.Text('Players', size = 30)
            lobby_player_list = ft.Text('', size=15)
            ready_list = ft.ElevatedButton(content=waitstart, on_click=lambda _: ready_up(user, ready_status),height=300)

            ready_container = ft.Container(height=100,
                                           margin=0,
                                           alignment=ft.alignment.center,
                                           content=ready_list)
            leave_container = ft.Container(height=100,
                                           margin=0,
                                           alignment=ft.alignment.center,
                                           content=ft.ElevatedButton("Leave Lobby", on_click=lambda _: leave_lobby(user)))
            bgspace= ft.Container(height=75,
                               margin=0,
                               alignment=ft.alignment.center,
                               content=ft.Text(""))

            space = ft.Container(height=175,
                               margin=0,
                               alignment=ft.alignment.center,
                               content=ft.Text(""))
            lobbytitle = ft.Text(f"Lobby {user.lobby[-1]}", size = 50)
            lobbycenter = ft.Container(alignment=ft.alignment.center,content=lobbytitle)
            backgroundcontainer = ft.Container(
                alignment=ft.alignment.center,
                content=ft.Column(
                    [bgspace, playertext, lobby_player_list]),
            )
            buttoncontainer = ft.Container(
                alignment=ft.alignment.bottom_center,
                content=ft.Column(
                    [lobbycenter, space,ready_status_container,ready_container, leave_container]),
            )
            page.views.append(
                ft.View(
                    "/waiting",
                    [
                        ft.Column([ft.Container(content=ft.Stack([
                            ft.Image(src='waiting.png',
                                     ), backgroundcontainer,buttoncontainer]))]),
                        # ft.Text(value=f'The word is {user.my_word}')
                        # ft.AppBar(title=ft.Text(f"Lobby {user.lobby[-1]}"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ]
                )
            )
            while True:
                time.sleep(1)
                player_list = requests.get(URL + '/players?lobby=' + user.lobby).json()
                if user.ready:
                    retrieve_word(user)
                    if user.my_word:
                        if '_' in user.my_word:
                            page.go('/liar')
                            break
                        else:
                            page.go('/player')
                            break
                lobby_player_list.value = '\n'.join(player_list)
                page.update()

        if page.route == "/liar":
            page.theme_mode = ft.ThemeMode.DARK
            pregame_time = ft.Text(value=f'{PREGAME_PAGE_TIME}', text_align=ft.TextAlign.CENTER, width=100)
            word = ft.Text(value=f'{user.my_word}')
            space = ft.Container(ft.Text(""),height=375)
            word_cont = ft.Container(alignment=ft.alignment.center,
                                     content=word)

            wordonbg = ft.Container(
                alignment=ft.alignment.center,
                content=ft.Column(
                    [space,word_cont]
                )
            )
            page.views.append(
                ft.View(
                    "/liar",
                    [
                        ft.Column([ft.Container(content=ft.Stack([
                            ft.Image(src='liarpage.png',
                                     ),wordonbg]))]),
                    ],
                )
            )
            page.update()
            general_timer(pregame_time, '/discussion')

        if page.route == "/player":
            page.theme_mode = ft.ThemeMode.LIGHT
            pregame_time = ft.Text(value=f'{PREGAME_PAGE_TIME}', text_align=ft.TextAlign.CENTER, width=100)
            word = ft.Text(value=f'{user.my_word}')
            space = ft.Container(ft.Text(""), height=430)
            word_cont = ft.Container(alignment=ft.alignment.center,
                                     content=word)

            wordonbg = ft.Container(
                alignment=ft.alignment.center,
                content=ft.Column(
                    [space, word_cont]
                )
            )
            page.views.append(
                ft.View(
                    "/player",
                    [
                        ft.Column([ft.Container(content=ft.Stack([
                            ft.Image(src='playerpage.png',
                                     ),wordonbg]))]),
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
            page.theme_mode = ft.ThemeMode.DARK
            vote_time = ft.Text(value=f'{VOTING_TIME}', text_align=ft.TextAlign.CENTER, size= 30)

            def send_vote(voted_player: str):
                ret = requests.post(URL + '/send_vote?lobby=' + user.lobby + '&voted_player=' + voted_player).json()
                page.go('/votedone')

            vote_time_container = ft.Container(height=375,
                                        alignment=ft.alignment.bottom_center,
                                        margin=0,
                                        content=vote_time,
                                        )
            bgspace= ft.Container(height=150,
                               margin=0,
                               alignment=ft.alignment.center,
                               content=ft.Text(""))

            backgroundcontainer = ft.Container(
                alignment=ft.alignment.center,
                content=ft.Column(
                    [bgspace, vote_time_container]),

            )
            buttoncontainer = ft.Container(
                alignment=ft.alignment.bottom_center,
                content=ft.Column(
                    []),
            )
            view = ft.View(
                "/voting",
                [ft.Column([ft.Container(content=ft.Stack([
                            ft.Image(src='vote.png',
                                     ), backgroundcontainer,buttoncontainer]))]),
                ],
            )

            player_list = requests.get(URL + '/liar_list?lobby=' + user.lobby).json() + requests.get(
                URL + '/players?lobby=' + user.lobby).json()
            player_list.remove(user.username)
            for player in player_list:
                vote_p_cont = ft.Container(
                             alignment=ft.alignment.center,
                             margin=-3,
                             content=ft.ElevatedButton(text=player,
                                                       on_click=lambda _,
                                                        p=player: send_vote(p)),
                             )
                buttoncontainer.content.controls.append(vote_p_cont)

            page.views.append(view)
            general_timer(vote_time, '/votedone')
            page.update()

            if int(vote_time.value) <= 0:
                state: str = requests.get(URL + '/get_game_state?lobby=' + user.lobby + '&player=' + user.username).json()
                if state == 'PLAYERWIN':
                    page.go('/playerwin')
                elif state == 'LIARWIN':
                    page.go('/liarwin')
                elif state == 'CONTINUE':
                    page.go('/continue')
                else:
                    # something fucked up
                    page.go('/')
                ret = requests.post(URL + '/reset_vote?lobby=' + user.lobby).json()

        if page.route == "/liarwin":
            status_time = ft.Text(value=f'{WINNER_TIME}', text_align=ft.TextAlign.CENTER, width=100)

            page.views.append(
                ft.View(
                    "/liarwin",
                    [
                        ft.Column([ft.Container(content=ft.Stack([
                            ft.Image(src='liarwin.PNG',
                                     ), ]))])
                    ],
                )
            )
            general_timer(status_time, '/')
            page.update()
            ret = requests.post(URL + '/reset_lobby?lobby=' + user.lobby).json()

        if page.route == "/playerwin":
            status_time = ft.Text(value=f'{WINNER_TIME}', text_align=ft.TextAlign.CENTER, width=100)

            page.views.append(
                ft.View(
                    "/playerwin",
                    [
                        ft.Column([ft.Container(content=ft.Stack([
                            ft.Image(src='pwin.png',
                                     ), ]))])
                    ],
                )
            )
            general_timer(status_time, '/')
            page.update()
            ret = requests.post(URL + '/reset_lobby?lobby=' + user.lobby).json()

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
                        ft.Image(src="continue.PNG"),
                        # status_time,
                    ],
                )
            )

            ret = requests.get(URL).json()
            if user.username in ret[user.lobby]['liars']:
                page_to_go = '/liar'
                user.my_word = requests.get(URL + '/get_word?lobby=' + user.lobby + '&player=' + user.username).json()
            elif user.username in ret[user.lobby]['active_players']:
                page_to_go = '/player'
                user.my_word = requests.get(URL + '/get_word?lobby=' + user.lobby + '&player=' + user.username).json()
            else:
                page_to_go = '/votedout'
            general_timer(status_time, page_to_go)
            page.update()

        if page.route == "/votedout":
            status_time = ft.Text(value=f'{VOTED_OUT_TIME}', text_align=ft.TextAlign.CENTER, width=100)
            page.views.append(
                ft.View(
                    "/votedout",
                    [
                        ft.Image(src='votedout.PNG'),
                        # status_time,
                    ],
                )
            )
            page.update()
            reset_player(user)
            general_timer(status_time, '/')


    def reset_player(player: User):
        player.lobby = None
        player.my_word = None

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



