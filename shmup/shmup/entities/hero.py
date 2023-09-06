from importlib import resources

import pygame

from shmup.config import cfg_item
from shmup.entities.gameobject  import GameObject

class Hero(GameObject):

    def __init__(self, screen):

        super().__init__()
        with resources.path(cfg_item("entities", "hero","image_file")[0],cfg_item("entities", "hero","image_file")[1]) as hero_file:
            self.__hero_image  =  pygame.image.load(hero_file).convert_alpha()

        self.__is_moving_left = False
        self.__is_moving_right = False
        self.__is_moving_up = False
        self.__is_moving_down = False

        self.__screen_width = screen.get_width()
        self.__screen_height = screen.get_height()

        self.__hero_image_half_width = self.__hero_image.get_width()/2
        self.__hero_image_half_height = self.__hero_image.get_height()/2
        self._position = pygame.math.Vector2(self.__screen_width/2,
                                                    self.__screen_height/2)
        self.render_rect = self.__hero_image.get_rect()
        self.rect = self.__hero_image.get_rect()
        self.rect.inflate(self.rect.width * - 0.60, self.rect.height - -0.20)
        self.__map_input()
        self._center()


    def handle_input(self,  key, is_pressed):
        if key == self.__key_mapping['left']:
            self.__is_moving_left = is_pressed
        if key == self.__key_mapping['right']:
            self.__is_moving_right = is_pressed    
        if key == self.__key_mapping['up']:
            self.__is_moving_up = is_pressed
        if key == self.__key_mapping['down']:
            self.__is_moving_down = is_pressed

    def update(self,delta_time):
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
            self._position += distance

        self._center()
    
    def render(self, surface_dst):
        surface_dst.blit(self.__hero_image, self.render_rect)

    def release(self):
        pass

    def __allow_move_inside_limits(self, movement):
        new_pos =  self._position + movement
        if (new_pos.x < -self.__hero_image_half_width ) or (new_pos.x >self.__screen_width - self.__hero_image_half_width ) or (new_pos.y < -self.__hero_image_half_height)  or (new_pos.y >self.__screen_height - self.__hero_image_half_height):
            return False
        
        return True
    
    def __map_input(self):
        key_mapping = cfg_item("input","key_mapping")
        self.__key_mapping = {}
        
        for k,v in key_mapping.items():
            self.__key_mapping[k] = pygame.key.key_code(v) 