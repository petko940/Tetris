import pygame

from game import Tetris

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 501
FONT = pygame.font.Font("files/menu_font.ttf", 29)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

start_surface = FONT.render("START", True, YELLOW)
exit_surface = FONT.render("EXIT", True, RED)


class Menu:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = pygame.image.load('files/menu_image.png')
        self.start_button_rect = pygame.Rect(155, 230, 89, 22)
        self.exit_button_rect = pygame.Rect(165, 287, 68, 22)

    def draw_buttons(self, x, y, surface):
        # pygame.draw.rect(
        #     self.screen,
        #     (255, 255, 255),
        #     self.start_button_rect
        # )
        # pygame.draw.rect(
        #     self.screen,
        #     (255, 255, 255),
        #     self.exit_button_rect
        # )
        self.screen.blit(surface, (x, y))

    def countdown_start(self):
        font = pygame.font.Font(None, 150)

        for i in range(3, 0, -1):
            self.screen.fill(BLACK)
            countdown_text = font.render(str(i), True, WHITE)
            countdown_rect = countdown_text.get_rect(center=self.screen.get_rect().center)
            self.screen.blit(countdown_text, countdown_rect)
            pygame.display.flip()
            pygame.time.wait(600)

        self.screen.fill(BLACK)
        pygame.display.flip()

    def exit_images(self, images):
        for image in images:
            self.screen.fill(BLACK)
            self.screen.blit(image, (0, 0))
            pygame.display.flip()
            pygame.time.wait(600)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button_rect.collidepoint(event.pos):
                        self.countdown_start()
                        game = Tetris()
                        game.run()
                    elif self.exit_button_rect.collidepoint(event.pos):
                        image_paths = [
                            "files/exit_images/1.png",
                            "files/exit_images/2.png",
                            "files/exit_images/3.png"
                        ]
                        images = [pygame.image.load(path) for path in image_paths]
                        self.exit_images(images)
                        exit()

            self.screen.blit(self.background, (0, 0))

            self.draw_buttons(
                self.start_button_rect.x,
                self.start_button_rect.y,
                start_surface
            )
            self.draw_buttons(
                self.exit_button_rect.x,
                self.exit_button_rect.y,
                exit_surface
            )

            pygame.display.flip()


menu = Menu()
menu.run()
