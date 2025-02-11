from typing import List

from pygame import Color, Surface, display

from models.entity import Entity

DEFAULT_HEIGHT = 300
DEFAULT_WIDTH  = 420
MARGIN_FACTOR  = 0.9

INFO_ERROR = -1


class Window:
    """Represents the entire window that the game is rendered in."""
    _window_surface: Surface = None
    _entities: List[Entity] = []

    def __init__(self):
        """Create a Window."""
        # initialize the display module if it hasn't been already
        display.init()
        # Set the window size to be some fraction of the screen if we can get the screen size. If not,
        # set it to some arbitrary default size
        info = display.Info()
        self._width = info.current_w * MARGIN_FACTOR if info.current_w != INFO_ERROR else DEFAULT_WIDTH
        self._height = info.current_h * MARGIN_FACTOR if info.current_h != INFO_ERROR else DEFAULT_HEIGHT
        self._window_surface = display.set_mode((self._width, self._height))

    def clear(self):
        """Clear all elements currently drawn to the window."""
        self._window_surface.fill(Color(0, 0, 0))

    def update(self):
        """Updates the contents of the entire window."""
        for entity in self._entities:
            entity.move()
            if entity.get_left() <= 0 or entity.get_right() >= self._width:
                entity.handle_window_border_x()
            if entity.get_top() <= 0 or entity.get_bottom() >= self._height:
                entity.handle_window_border_y()
            # blit means to actually draw the entity onto the screen
            self._window_surface.blit(entity.get_surface(), entity.get_rect())
        # flip redraws the window
        display.flip()

    def register_entity(self, entity: Entity):
        """Register a new entity to be managed by the window."""
        self._entities.append(entity)
