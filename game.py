"""
Developed By:
Keerthi koushik devulapally
Nikhil reddy jitta
Ranjith reddy pingli
Neelima vuyyuru
Paladi Mahesh Gowtham
"""

from dataclasses import dataclass, field
from random import randrange
from time import sleep
from typing import Any, List

# from pygame import init as pg_init, display as pg_display, image as pg_image, Surface as PG_Surface, font
import pygame
import pygame_menu
from pygame_menu.examples import create_example_window

from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from levels.level1 import Level
from resources.dimension import Dimensions



DIFFICULTY = ['EASY']
DIMS=[3]
ROWS=[3]
COLUMNS=[3]
PLAYERS=[2]
FPS = 60


@dataclass
class Scores:
    
    difficulty: str = ""
    max: int = 0 
    min: int = 0
    attempt: int = 0


@dataclass
class Game:

    menu_states: List[str] = field(init=False)
    screen: pygame.Surface = field(init=False)
    play_menu: Any = field(init=False)
    stats: List[Scores] =  field(init=False)
    is_running: bool = True
    is_paused: bool = True
    display_caption_prefix: str = "Lost in Woods"

    # define a system wide theme
    game_theme = pygame_menu.themes.Theme(
            background_color=(102,102,255),
            title_font_color=(0,0,0),
            title_background_color=(200,200,0),
            widget_font_size=30,
            widget_padding=5)
    selected_menu_state: str = 'main'

    auto_play: bool = False
    selected_level: str = 'EASY'



    def background(self):
        global surface
        surface.fill((0,0,0))


    def set_score(self,index,score):
            self.stats[index].attempt +=1
            self.stats[index].min = min(score, self.stats[index].min) if self.stats[index].min !=0 else score
            self.stats[index].max = max(score, self.stats[index].max) if self.stats[index].max !=0 else score

            try:
                with open(f'./score/scores{index}.txt','w') as file:
                    file.write(f"{self.stats[index].attempt}\n")
                    file.write(f"{self.stats[index].min}\n")
                    file.write(f"{self.stats[index].max}\n")
            except: 
                print("File not found")


    def game_play(self,difficulty: List, font: 'pygame.font.Font', test: bool = False) -> None:
        """
        Main game function.
        :param difficulty: Difficulty of the game
        :param font: Pygame font
        :param test: Test method, if ``True`` only one loop is allowed
        """
        assert isinstance(difficulty, list)
        difficulty = difficulty[0]
        assert isinstance(difficulty, str)

        # Define globals
        global main_menu
        global clock


        if difficulty == 'EASY':
            level = Level(autoplay=False,dimensions= Dimensions(COLUMNS[0],ROWS[0]),number_of_players= PLAYERS[0])
            score = level.start(clock)
        elif difficulty == 'MEDIUM':
            level = Level(autoplay=False,dimensions= Dimensions(COLUMNS[0],ROWS[0]),number_of_players= PLAYERS[0])
            score = level.start(clock)
        elif difficulty == 'HARD':
            level = Level(autoplay=False,dimensions= Dimensions(COLUMNS[0],ROWS[0]),number_of_players= PLAYERS[0])
            score = level.start(clock)
        else:
            raise ValueError(f'unknown difficulty {difficulty}')
        f_esc = font.render('Game Ended', True, (255, 255, 255))

        if self.selected_level == "EASY":
            self.set_score(0,score)
        if self.selected_level == "MEDIUM":
            self.set_score(1,score)
        if self.selected_level == "HARD":
            self.set_score(2,score)

        bg_color = (0,0,0)
        self.game_menu()
        # Reset main menu and disable
        # You also can set another menu, like a 'pause menu', or just use the same
        # main_menu as the menu that will check all your input.

        self.game_theme = pygame_menu.themes.THEME_DEFAULT.copy()
        main_menu = pygame_menu.Menu(
            height=WINDOW_HEIGHT * 0.6,
            theme=self.game_theme,
            title='Main Menu',
            width=WINDOW_WIDTH * 0.6
        )
        main_menu.add.button('Play', self.play_menu)

        main_menu.add.selector('Difficulty ',
                            [('Easy', 'EASY'),
                                ('Medium', 'MEDIUM'),
                                ('Hard', 'HARD')],
                            onchange=self.set_difficulty,
                            selector_id='select_difficulty')
        main_menu.add.button('Quit', pygame_menu.events.EXIT)

        main_menu.enable()

        while True:
            clock.tick(60)
            events = pygame.event.get()
            for e in events:
                if e.type == pygame.QUIT:
                    exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        main_menu.enable()
                        return
                        
            if main_menu.is_enabled():
                main_menu.update(events)

            surface.fill(bg_color)

            surface.blit(f_esc, (int((WINDOW_WIDTH - f_esc.get_width()) / 2),
                                int(WINDOW_HEIGHT / 2 + f_esc.get_height())))
            pygame.display.flip()


    def set_difficulty(self,value, difficulty) -> None:
        self.selected_level=difficulty
        DIFFICULTY[0] = difficulty


    def set_rows(self,value, row) -> None:
        ROWS[0] = row


    def set_columns(self,value, col) -> None:
        COLUMNS[0] = col

    def change_dims(self,value, col) -> None:
        DIMS[0] = col
        
    def set_players(self,value, players) -> None:
        PLAYERS[0] = players

    def game_menu(self):

        submenu_theme = pygame_menu.themes.THEME_DARK.copy()
        self.play_menu = pygame_menu.Menu(
            height=WINDOW_HEIGHT * 0.7,
            title='Play Menu',
            width=WINDOW_WIDTH * 0.75,
            theme= self.game_theme
        )
        play_submenu = pygame_menu.Menu(
            height=WINDOW_HEIGHT * 0.5,
            theme=self.game_theme,
            title='Scores',
            width=WINDOW_WIDTH * 0.7
        )


        for stat in self.stats:
                min = stat.min
                max = stat.max
                attempt = stat.attempt
                play_submenu.add.button(f'{stat.difficulty.lower()} Played {attempt}', pygame_menu.events.BACK) 
                play_submenu.add.button(f'{stat.difficulty.lower()} Highest {min} ', pygame_menu.events.BACK)
                play_submenu.add.button(f'{stat.difficulty.lower()} Lowest {max} ', pygame_menu.events.BACK)   
        play_submenu.add.button('Back to menu', pygame_menu.events.RESET)

        self.play_menu.add.selector('Rows: ',
                    [('2',2),('3',3),('4',4),('5',5),('6',6),('7',7),('8',8),('9',9)],
                    onchange=self.set_rows,
                    selector_id='select_row')
        self.play_menu.add.selector('Columns: ',
                        [('2',2),('3',3),('4',4),('5',5),('6',6),('7',7),('8',8),('9',9)],                      
                    onchange=self.set_columns,
                    selector_id='select_cols')
        self.play_menu.add.selector('Players: ',
                        [('2',2),('3',3),('4',4)],
                    onchange=self.set_players,
                    selector_id='select_players')
        self.play_menu.add.button('Scores', play_submenu)
        self.play_menu.add.button('Start',  # When pressing return -> play(DIFFICULTY[0], font)
                         self.game_play,
                         DIFFICULTY,
                            pygame.font.Font(pygame_menu.font.FONT_FRANCHISE, 30))
        self.play_menu.add.button('Back to menu', pygame_menu.events.BACK)



    def start_menu(self):

        global clock
        global main_menu
        global surface

        surface = create_example_window('Lost in the Woods', (WINDOW_WIDTH,WINDOW_HEIGHT))
        clock = pygame.time.Clock()


        self.game_menu()

        main_menu = pygame_menu.Menu(
            height=WINDOW_HEIGHT * 0.6,
            theme=self.game_theme,
            title='Menu',
            width=WINDOW_WIDTH * 0.6
        )
                    
        self.game_theme.widget_font_size = 19
        

        main_menu.add.selector('Difficulty ',
                            [('Easy', 'EASY'),
                                ('Medium', 'MEDIUM'),
                                ('Hard', 'HARD')],
                            onchange=self.set_difficulty,
                            selector_id='select_difficulty',
                            font_size=25, border_width=1,)
        main_menu.add.button('Play', self.play_menu, font_color=(0,0,0), font_size=30, border_width=1,)
        main_menu.add.button('Exit', pygame_menu.events.EXIT, font_color=(0,0,0), font_size=35, border_width=1,)

    def get_score(self):
        data0 = [0 for i in range(3)]
        data1 = [0 for i in range(3)]
        data2 = [0 for i in range(3)]
        try:
            with open('./score/scores0.txt') as f:
                lines = f.readlines()
                for k,v in enumerate(lines):
                    data0[k] = round(float(v.strip()))
            with open('./score/scores1.txt') as f:
                lines = f.readlines()
                for k,v in enumerate(lines):
                    data1[k] = round(float(v.strip()))
            with open('./score/scores2.txt') as f:
                lines = f.readlines()
                for k,v in enumerate(lines):
                    data2[k] = round(float(v.strip()))
        except FileNotFoundError:
            print("File not found")
    
        self.stats = [ 
            Scores('EASY',data0[0],data0[1],data0[2]),
            Scores('MEDIUM',data1[0],data1[1],data1[2]),
            Scores('HARD',data2[0],data2[1],data2[2]),
        ]



    def start(self):
        pygame.init()
        pygame.mixer.init()
        self.get_score()
        self.start_menu()
        pygame.mixer.music.load('./assets/audio.mp3')
        pygame.mixer.music.play(loops=0)
      
        while True:

            # Tick
            clock.tick(FPS)

            # Paint background
            self.background()

            # Application events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            # Main menu
            if main_menu.is_enabled():
                main_menu.mainloop(surface, self.background, disable_loop=False, fps_limit=FPS)

            # Flip surface
            pygame.display.flip()

## start the game
if __name__ == "__main__":
    game = Game()
    game.start()
