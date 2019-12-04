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


class SpriteBase(pygame.sprite.Sprite):
    def __init__(self, init_x, init_y):
        super().__init__()

        self.image_path = ''  # TODO: fill me
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.width, self.height = self.image.get_size()

        # If mask collision is intended
        self.mask = pygame.mask.from_surface(self.image)

        # Attributes
        self.position = (init_x, init_y)
        self.speed = None  # TODO: fill me

        self.rect = self.get_rect()

    def get_rect(self):
        return self.image.get_rect(center=self.position)

    def update(self, pressed_keys):
        if pressed_keys[pygame.K_UP]:
            # Update attributes here based on events
            pass

        # self.kill()

        self.rect = self.get_rect()

    def is_collision(self, x, y):
        x -= self.rect.x
        y -= self.rect.y

        if 0 < x < self.width and 0 < y < self.height:
            return self.mask.get_at((x, y))


class Screen:
    def __init__(self, screen_size, background_color):
        self.size = screen_size
        self.background_color = background_color

        self.surface = pygame.display.set_mode(self.size, 0, 32)
        self.surface_background = None

        pygame.display.set_caption('Title')
        # icon = pygame.image.load('icon.png')
        # pygame.display.set_icon(icon)

        self.init(background_color)

    def init(self, background_color):
        self.surface.fill(background_color)

        # Draw background screen/sprites here

        # Set screen background
        self.set_surface_background()

    def set_surface_background(self):
        self.surface_background = self.surface.copy()

    def render_text(self, text, position):
        self.surface.blit(text, position)


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
            self.screen.surface,
            self.screen.surface_background
        )

        # Update sprites
        for entity in self.all_sprites:
            entity.update(keys)

        # Draw sprites
        self.all_sprites.draw(self.screen.surface)

        pygame.display.update()

    def main(self):
        # Custom events
        my_event = pygame.USEREVENT + 1
        pygame.time.set_timer(my_event, 250)

        while self.running:

            mouse_button = mouse_x = mouse_y = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

                elif event.type == pygame.MOUSEBUTTONUP:
                    mouse_x, mouse_y = event.pos
                    if event.button == MOUSE_LEFT:
                        mouse_button = MOUSE_LEFT

            keys = pygame.key.get_pressed()

            # Mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            self.update_frame(keys)

            self.clock.tick(FPS)


# Run
if __name__ == '__main__':
    pygame.init()
    gui = GUI(SCREEN_SIZE)
    gui.main()
    pygame.quit()
