import pygame

# CONSTANTS
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


def update_screen(screen, all_sprites, keys):
    screen.fill(COLORS['WHITE'])

    for entity in all_sprites:
        entity.update(keys)
        screen.blit(entity.image, entity.rect)

    pygame.display.update()


def main():
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
    pygame.display.set_caption('Game')

    fps_clock = pygame.time.Clock()

    # Custom events
    MYEVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENT, 250)

    all_sprites = pygame.sprite.Group()

    running = True

    while running:
        fps_clock.tick(FPS)

        mouse_x, mouse_y = 0, 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == MOUSE_LEFT:
                    mouse_x, mouse_y = event.pos

        keys = pygame.key.get_pressed()

        update_screen(screen, all_sprites, keys)

    pygame.quit()


# Run
if __name__ == '__main__':
    main()
