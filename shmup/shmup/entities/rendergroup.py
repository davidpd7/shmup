import pygame

class RenderGroup(pygame.sprite.Group):

    def input(self, key, is_pressed):
        for sprite in self.sprites():
            sprite.handle_input(key, is_pressed)


    def draw(self, surface):
        for sprite in self.sprites():
            sprite.render(surface)  
    


            