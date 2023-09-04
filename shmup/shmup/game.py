import os

import pygame

from shmup.fps_stats import FPSStats
from shmup.config import Config

class Game:

    __key_maping = {"left": pygame.K_LEFT, 
                "right": pygame.K_RIGHT,
                "up":pygame.K_UP,
                "down":pygame.K_DOWN},

    def __init__(self):
        
        pygame.init()
        self.__screen = pygame.display.set_mode(Config.screen_size, 0, 32)
        pygame.display.set_caption(Config.game_caption)
        self.__hero_image  =  pygame.image.load(os.path.join(*Config.hero_image_path)).convert_alpha()

        font = pygame.font.Font(os.path.join(*Config.font_path))
        self.__my_text = font.render(Config.message, 
                                     True, 
                                     Config.font_foreground_color, 
                                     Config.background_color)
        self.__running = True
        self.__hero_image_half_width = self.__hero_image.get_width()/2
        self.__hero_image_half_height = self.__hero_image.get_height()/2

        self.__fps_stats = FPSStats(font)

        self.__is_moving_left = False
        self.__is_moving_right = False
        self.__is_moving_up = False
        self.__is_moving_down = False

        self.__hero_position = pygame.math.Vector2(self.__screen.get_width()/2 - self.__hero_image_half_width,
                                                  self.__screen.get_height()/2 - self.__hero_image_half_height)
      
    def run(self):
         
        last_time  = pygame.time.get_ticks()
        time_since_last_update = 0
        while self.__running: 
            delta_time, last_time = self.__calc_delta_time(last_time)
            time_since_last_update += delta_time                                           
            while time_since_last_update > Config.time_per_frame:
                time_since_last_update -= Config.time_per_frame
                self.__process_event()
                self.__update(Config.time_per_frame)
            self.__render()
        
        self.__quit()
    
    def __process_event(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                if event.type == pygame.KEYDOWN:
                    self.__handle_player_input(event.key, True)
                if event.type == pygame.KEYUP:
                    self.__handle_player_input(event.key, False)


    def __handle_player_input(self, key, is_pressed):
        if key == Game.__key_maping['left']:
            self.__is_moving_left = is_pressed
        if key == Game.__key_maping['right']:
            self.__is_moving_right = is_pressed    
        if key == Game.__key_maping['up']:
            self.__is_moving_up = is_pressed
        if key == Game.__key_maping['down']:
            self.__is_moving_down = is_pressed

    def __update(self, delta_time):

        speed = pygame.math.Vector2(0.0,0.0)

        if self.__is_moving_left:
            speed.x -=  Config.hero_speed
        if self.__is_moving_right:
            speed.x += Config.hero_speed 
        if self.__is_moving_up:
            speed.y -= Config.hero_speed
        if self.__is_moving_down:
            speed.y += Config.hero_speed
    
        distance = speed * delta_time
        
        if self.__allow_move_inside_limits(distance):
            self.__hero_position += distance
        
        self.__fps_stats.update(delta_time)

    def __render(self):
    
        self.__screen.fill(Config.background_color)
        self.__screen.blit(self.__hero_image, self.__hero_position.xy)
        self.__fps_stats.render(self.__screen)

        pygame.display.update()

    def __quit(self):
        pygame.quit()


    def __allow_move_inside_limits(self, movement):
        new_pos =  self.__hero_position + movement
        if (new_pos.x < -self.__hero_image_half_width ) or (new_pos.x >self.__screen.get_width() - self.__hero_image_half_width ) or (new_pos.y < -self.__hero_image_half_height)  or (new_pos.y >self.__screen.get_height() - self.__hero_image_half_height):
            return False
        
        return True
    
    def __calc_delta_time(self, last_time):
        current = pygame.time.get_ticks()
        delta = current - last_time
        return delta, current