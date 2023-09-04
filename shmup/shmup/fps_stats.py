class FPSStats:

    __background_color = (82,31,145)
    __foreground_color = (255,255,255)
    __pos = (0,0)
    __max_update_time = 1000

    def __init__(self, font):
            self.__font = font
            self.__logic_frames = 0
            self.__render_frames = 0
            self.__update_time = 0
            self.__set_fps_surface()


    def update(self, delta_time):
        self.__logic_frames += 1 
        self.__update_time += delta_time

        if self.__update_time >= FPSStats.__max_update_time:
             self.__set_fps_surface()
             self.__logic_frames = 0
             self.__render_frames = 0
             self.__update_time -= FPSStats.__max_update_time
             
    def render(self, surface):
        self.__render_frames += 1
        surface.blit(self.__fps_surface, FPSStats.__pos)

    def __set_fps_surface(self):
           self.__fps_surface = self.__font.render(f"Update {self.__logic_frames} - Render {self.__render_frames}", 
                                                   True, FPSStats.__foreground_color, FPSStats.__background_color)         