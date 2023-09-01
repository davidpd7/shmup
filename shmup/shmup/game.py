import os

import pygame

class Game:

    __game_caption = "David"
    __hero_image_path = ['shmup','assets', 'images', 'images.png']
    __font_path = ['shmup','assets', 'fonts', 'Sansation.ttf'] 
    __screen_size = (640,480)
    __background_color = (82,31,145)
    __font_foreground_color = (255,255,255)
    __message = "Game"
    __mesage_location = (10,10)
    __hero_speed = 0.5
    __key_maping = {"left": pygame.K_LEFT, 
                        "right": pygame.K_RIGHT,
                        "up":pygame.K_UP,
                        "down":pygame.K_DOWN}
    __fps_clock = 60


    def __init__(self):
        
        pygame.init()
        self.__screen = pygame.display.set_mode(Game.__screen_size, 0, 32)
        pygame.display.set_caption(Game.__game_caption)
        self.__hero_image  =  pygame.image.load(os.path.join(*Game.__hero_image_path)).convert_alpha()

        font = pygame.font.Font(os.path.join(*Game.__font_path))
        self.__my_text = font.render(Game.__message, 
                                     True, 
                                     Game.__font_foreground_color, 
                                     Game.__background_color)
        self.__running = True
        self.__hero_image_half_width = self.__hero_image.get_width()/2
        self.__hero_image_half_height = self.__hero_image.get_height()/2

        self.__is_moving_left = False
        self.__is_moving_right = False
        self.__is_moving_up = False
        self.__is_moving_down = False

        self.__hero_position = pygame.math.Vector2(self.__screen.get_width()/2 - self.__hero_image_half_width,
                                                  self.__screen.get_height()/2 - self.__hero_image_half_height)
      


    def run(self):
        
        fps_clock = pygame.time.Clock()
        while self.__running:
            delta_time = fps_clock.tick(Game.__fps_clock)
            self.__process_event()
            self.__update(delta_time)
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
            speed.x -=  Game.__hero_speed
        if self.__is_moving_right:
            speed.x += Game.__hero_speed 
        if self.__is_moving_up:
            speed.y -= Game.__hero_speed
        if self.__is_moving_down:
            speed.y += Game.__hero_speed
    
        distance = speed * delta_time
        
        if self.__allow_move_inside_limits(distance):
            self.__hero_position += distance



    def __render(self):
        x,y = pygame.mouse.get_pos()
        self.__screen.fill(Game.__background_color)
        x -= self.__hero_image_half_width
        y -= self.__hero_image_half_height
        self.__screen.blit(self.__hero_image, self.__hero_position.xy)
        self.__screen.blit(self.__my_text, Game.__mesage_location)
        pygame.display.update()

        
    def __quit(self):
        pygame.quit()


    def __allow_move_inside_limits(self, movement):
        new_pos =  self.__hero_position + movement
        if (new_pos.x < -self.__hero_image_half_width ) or (new_pos.x >self.__screen.get_width() - self.__hero_image_half_width ) or (new_pos.y < -self.__hero_image_half_height)  or (new_pos.y >self.__screen.get_height() - self.__hero_image_half_height):
            return False
        
        return True
    