import os

import pygame

# CONSTANTS
SOURCE_PATH = 'src'

MOUSE_LEFT = 1
MOUSE_RIGHT = 3

FPS = 30

SCREEN_SIZE = (800, 600)

COLORS = {
    'BLACK': (0, 0, 0),
    'WHITE': (255, 255, 255),
    'GRAY': (128, 128, 128),
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 155),
    'YELLOW': (255, 255, 0)
}


class Entity(pygame.sprite.Sprite):
    def __init__(self, init_x, init_y):
        super().__init__()

        self.image_path = ''  # TODO: fill me
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.rect = self.image.get_rect(center=(init_x, init_y))

        # If mask collision is intended
        self.mask = pygame.mask.from_surface(self.image)

        self.speed = None  # TODO: fill me

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_UP]:
            pass

        # self.kill()


class Screen:
    def __init__(self, screen_size, background_color):
        self.screen_size = screen_size
        self.screen_bg_color = background_color

        self.screen_surface = pygame.display.set_mode(self.screen_size, 0, 32)
        pygame.display.set_caption('Title')
        # icon = pygame.image.load('icon.png')
        # pygame.display.set_icon(icon)

        self.screen_surface_background = None

        self.init_screen(background_color)

    def init_screen(self, background_color):
        self.screen_surface.fill(background_color)

        # Draw background screen

        # Set screen background
        self.screen_surface_background = self.screen_surface.copy()


class GUI:
    def __init__(self, screen_size, background_color=COLORS['WHITE']):
        self.source_path = os.path.join(os.getcwd(), SOURCE_PATH)

        self.running = True

        self.screen = Screen(screen_size, background_color)

        self.all_sprites = pygame.sprite.Group()

        self.clock = pygame.time.Clock()

    def update_frame(self, keys):
        # Clear sprites on previous frame
        self.all_sprites.clear(
            self.screen.screen_surface,
            self.screen.screen_surface_background
        )

        # Update sprites
        for entity in self.all_sprites:
            entity.update(keys)

        # Draw sprites
        self.all_sprites.draw(self.screen.screen_surface)

        pygame.display.update()

    def main(self):
        # Custom events
        MYEVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(MYEVENT, 250)

        while self.running:

            mouse_x = mouse_y = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == MOUSE_LEFT:
                        mouse_x, mouse_y = event.pos

            keys = pygame.key.get_pressed()

            self.update_frame(keys)

            self.clock.tick(FPS)


# Run
if __name__ == '__main__':
    pygame.init()
    gui = GUI(SCREEN_SIZE)
    gui.main()
    pygame.quit()
