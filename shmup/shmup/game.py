from importlib import resources

import pygame

from shmup.fps_stats import FPSStats
from shmup.config import cfg_item

class Game:

    def __init__(self):

        pygame.init()
        self.__screen = pygame.display.set_mode(cfg_item("game","screen_size"), 0, 32)
        pygame.display.set_caption(cfg_item("game","game_caption"))

        with resources.path(cfg_item("entities", "hero","image_file")[0],cfg_item("entities", "hero","image_file")[1]) as hero_file:
            self.__hero_image  =  pygame.image.load(hero_file).convert_alpha()
        
        with resources.path(cfg_item("font","file")[0],cfg_item("font","file")[1]) as font_file:
            font = pygame.font.Font(font_file)
        self.__my_text = font.render(cfg_item("game","message"), 
                                        True, 
                                        cfg_item("font","font_foreground_color"), 
                                        cfg_item("game","background_color"))
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

        self.__map_input()
      
    def run(self):
        last_time  = pygame.time.get_ticks()
        time_since_last_update = 0
        while self.__running: 
            delta_time, last_time = self.__calc_delta_time(last_time)
            time_since_last_update += delta_time                                           
            while time_since_last_update > cfg_item("timing","time_per_frame"):
                time_since_last_update -= cfg_item("timing","time_per_frame")
                self.__process_event()
                self.__update(cfg_item("timing","time_per_frame"))
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
        if key == self.__key_mapping['left']:
            self.__is_moving_left = is_pressed
        if key == self.__key_mapping['right']:
            self.__is_moving_right = is_pressed    
        if key == self.__key_mapping['up']:
            self.__is_moving_up = is_pressed
        if key == self.__key_mapping['down']:
            self.__is_moving_down = is_pressed

    def __update(self, delta_time):

        speed = pygame.math.Vector2(0.0,0.0)

        if self.__is_moving_left:
            speed.x -=  cfg_item("entities","hero","speed")
        if self.__is_moving_right:
            speed.x +=  cfg_item("entities","hero","speed")
        if self.__is_moving_up:
            speed.y -=  cfg_item("entities","hero","speed")
        if self.__is_moving_down:
            speed.y +=  cfg_item("entities","hero","speed")
    
        distance = speed * delta_time
        
        if self.__allow_move_inside_limits(distance):
            self.__hero_position += distance
        
        self.__fps_stats.update(delta_time)

    def __render(self):
    
        self.__screen.fill(cfg_item("game","background_color"))
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
    
    def __map_input(self):
        key_mapping = cfg_item("input","key_mapping")
        self.__key_mapping = {}
        
        for k,v in key_mapping.items():
            self.__key_mapping[k] = pygame.key.key_code(v) 
