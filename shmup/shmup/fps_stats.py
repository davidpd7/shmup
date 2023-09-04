from shmup.config import cfg_item

class FPSStats:

    def __init__(self, font):
            self.__font = font
            self.__logic_frames = 0
            self.__render_frames = 0
            self.__update_time = 0
            self.__set_fps_surface()

    def update(self, delta_time):
        self.__logic_frames += 1 
        self.__update_time += delta_time

        if self.__update_time >= cfg_item("max_update_time"):
             self.__set_fps_surface()
             self.__logic_frames = 0
             self.__render_frames = 0
             self.__update_time -= cfg_item("max_update_time")
             
    def render(self, surface):
        self.__render_frames += 1
        surface.blit(self.__fps_surface, cfg_item("pos"))

    def __set_fps_surface(self):
           self.__fps_surface = self.__font.render(f"Update {self.__logic_frames} - Render {self.__render_frames}", 
                                                   True, cfg_item("font_foreground_color"), cfg_item("background_color"))