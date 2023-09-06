from importlib import resources
import random

import pygame

from shmup.fps_stats import FPSStats
from shmup.config import cfg_item
from shmup.entities.hero import Hero
from shmup.entities.rendergroup import RenderGroup
from shmup.entities.enemy import Enemy

class Game:

    def __init__(self):

        pygame.init()
        self.__screen = pygame.display.set_mode(cfg_item("game","screen_size"), 0, 32)
        pygame.display.set_caption(cfg_item("game","game_caption"))

        
        with resources.path(cfg_item("font","file")[0],cfg_item("font","file")[1]) as font_file:
            font = pygame.font.Font(font_file)

        self.__running = True
        
        self.__fps_stats = FPSStats(font)
        self.__hero = Hero(self.__screen)
        self.__player = RenderGroup()
        self.__player.add(Hero(self.__screen))
        self.__enemies = RenderGroup()
        self.__allied_projectiles = RenderGroup()
        self.__enemy_projectiles = RenderGroup()
      
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
                    self.__player.input(event.key, True)
                if event.type == pygame.KEYUP:
                    self.__player.input(event.key, False)

    def __update(self,  delta_time): 
        self.__player.update(delta_time)
        self.__enemies.update(delta_time)
        self.__allied_projectiles.update(delta_time)
        self.__enemy_projectiles.update(delta_time)
        self.__fps_stats.update(delta_time)
        self.__check_colisions()

        self.spawn_enemies()

    def __render(self):
    
        self.__screen.fill(cfg_item("game","background_color"))
        self.__player.draw(self.__screen)
        self.__enemies.draw(self.__screen)
        self.__allied_projectiles.draw(self.__screen)
        self.__enemy_projectiles.draw(self.__screen)
        self.__fps_stats.render(self.__screen)
        pygame.display.update()

    def __quit(self):
        self.__player.empty()
        self.__enemies.empty()
        self.__allied_projectiles.empty()
        self.__enemy_projectiles.empty()
        
        pygame.quit()

    
    def __calc_delta_time(self, last_time):
        current = pygame.time.get_ticks()
        delta = current - last_time
        return delta, current
    

    def spawn_enemies(self):
        if random.random() < cfg_item("entities", "enemies", "spawn_prob"):
            self.__enemies.add(Enemy())
    
    
    def __check_colisions(self):
        pygame.sprite.groupcollide(self.__player, self.__enemies, False, True)