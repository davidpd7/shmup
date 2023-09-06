
from importlib import resources
import random

import pygame

from shmup.config import cfg_item
from shmup.entities.gameobject  import GameObject

class Enemy(GameObject):

   

    def __init__(self):
        super().__init__()
        with resources.path(cfg_item("entities", "enemies","image_file")[0],cfg_item("entities", "enemies","image_file")[1]) as enamy_file:
            self.__enemy_image  =  pygame.image.load(enamy_file).convert_alpha()
        
        self.__enemy_image_half_width = self.__enemy_image.get_width()/2
        self.__enemy_image_half_height = self.__enemy_image.get_height()/2
        x_pos = random.randrange(self.__enemy_image_half_width, cfg_item("game", "screen_size")[0] - self.__enemy_image_half_width)
        y_pos = -self.__enemy_image.get_height()

        self._position = pygame.math.Vector2(x_pos,y_pos)

        self.render_rect = self.__enemy_image.get_rect()
        self.rect = self.__enemy_image.get_rect()

        self._center()
        
        self.__speed_y = random.uniform(cfg_item("entities", "enemies", "speed_range")[0],cfg_item("entities", "enemies", "speed_range")[1])
    
    def handle_input(self, key, is_pressed):
        pass

        
    def update(self, delta_time):
        distance_y = self.__speed_y * delta_time
        self._position.y += distance_y
        self._center()

        if self._position.y > cfg_item("game", "screen_size")[1] + self.__enemy_image.get_height():
            self.kill()

    
    def render(self, surface_dst):
        surface_dst.blit(self.__enemy_image, self.render_rect)


    def release(self):
        pass