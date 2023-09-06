from abc import ABC, abstractmethod
import pygame

class GameObject(ABC, pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self._position = pygame.Vector2(0,0)
        self.render_rect = pygame.Rect(0,0,0,0)
        self.rect = pygame.Rect(0,0,0,0)

    @abstractmethod
    def handle_input(self, key, is_pressed):
        pass

    @abstractmethod 
    def update(self, delta_time):
        pass

    @abstractmethod
    def render(self, serface_dst):
        pass

    @abstractmethod 

    def release(self):
        pass


    def _center(self):
        self.render_rect.center = self._position.xy
        self.rect.center = self._position.xy