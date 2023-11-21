import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import Gamestats
from button import Button
from scoreboard import Scoreboard

def rungame():
    # screen display
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.width, ai_settings.height))
    pygame.display.set_caption("Alien Invasion")
    ship=Ship(ai_settings,screen)
    bullets=Group()
    aliens=Group()
    stats=Gamestats(ai_settings)
    gf.create_fleet(ai_settings,screen,ship,aliens)
    play_button=Button(ai_settings,screen,"PLAY")
    sb=Scoreboard(ai_settings,screen,stats)
    # main loop
    while True:

        gf.check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets,sb)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,ship,bullets,aliens,stats,sb)
            gf.update_aliens(ai_settings,stats,screen,ship,aliens,bullets,sb)
        gf.update_screen(ai_settings,screen,stats,play_button,ship,aliens,bullets,sb)


rungame()