import pygame
import sys

from bullet import Bullet
from alien import Alien
from time import sleep

def fire_bullet(ai_settings,screen,ship,bullets):
    if len(bullets)<ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keydown_events(event,ai_settings,screen,ship,bullets):
    #respond to keypress
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key==pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()
def check_keyup_events(event,ship):
    #respond to keyrelease
    if event.key==pygame.K_RIGHT:
        ship.moving_right=False
    if event.key==pygame.K_LEFT:
        ship.moving_left=False

def check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets,sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,play_button,ship,aliens,bullets,sb,mouse_x,mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)

        elif event.type==pygame.KEYUP:
            check_keyup_events(event,ship)

def check_play_button(ai_settings,screen,stats,play_button,ship,aliens,bullets,sb,mouse_x,mouse_y):
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(False)
        ai_settings.initialize_dynamic_settings()

        #Reset game stats
        stats.reset_stats()
        stats.game_active=True

        #Reset scoreboard
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ship()

        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
def update_screen(ai_settings,screen,stats,play_button,ship,aliens,bullets,sb):
    # background color and ship
    screen.fill(ai_settings.bgcolor)
    #draw bullets
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    sb.draw_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

def update_bullets(ai_settings,screen,ship,bullets,aliens,stats,sb):
    #delete the bullets
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collision(ai_settings,screen,ship,bullets,aliens,stats,sb)


def get_number_alien_x(ai_settings,alien_width):
    available_space_x = ai_settings.width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x

def get_number_rows(ai_settings,ship_height,alien_height):
    available_space_y= ai_settings.height - 3*alien_height -ship_height
    number_rows= int(available_space_y/(2*alien_height))
    return number_rows

def create_alien(ai_settings,screen,aliens,alien_number,row_number,ship):
    alien = Alien(ai_settings, screen)
    alien_width=alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y=ship.rect.height + 2*alien.rect.height*row_number
    aliens.add(alien)

def create_fleet(ai_settings,screen,ship,aliens):
    alien=Alien(ai_settings,screen)
    number_alien_x=get_number_alien_x(ai_settings,alien.rect.width)
    number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number,ship)

def update_aliens(ai_settings,stats,screen,ship,aliens,bullets,sb):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()

    check_aliens_bottom(ai_settings,stats, screen, ship, aliens, bullets,sb)

def change_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y+=ai_settings.fleet_drop_factor
    ai_settings.fleet_direction*=-1

def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def check_bullet_alien_collision(ai_settings,screen,ship,bullets,aliens,stats,sb):
    collissions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collissions:
        for aliens in collissions.values():
            stats.score+=ai_settings.alien_points*len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level+=1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets,sb):
    if stats.ships_left>0:
        stats.ships_left-=1
        sb.prep_ship()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active=False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets,sb):
    ship_top=ship.ship_top
    for alien in aliens.sprites():
        if alien.rect.bottom>=ship_top:
            ship_hit(ai_settings,stats,screen,ship,aliens,bullets,sb)
            break

def check_high_score(stats,sb):
    if stats.high_score<stats.score:
        stats.high_score=stats.score
        sb.prep_high_score()