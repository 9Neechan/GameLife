import time
import pygame
import numpy as np

COLOR_BG = (10, 10, 10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
COLOR_ALIVE_NEXT = (255, 255, 255)


# фунуция, содержащая в себе главную логику раскрашивания клеток
def update(screen, cells, size, with_progress=False):
    update_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        # кол-во живых клеток
        alive = np.sum(cells[row - 1:row + 2, col - 1:col + 2]) - cells[row, col]
        # красим клетки в зависмотсти от их состояния
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT

        # реализуем правила игры
        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = COLOR_DIE_NEXT
            elif 2 <= alive <= 3:
                update_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
        else:
            if alive == 3:
                update_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT

        # раскрашиваем клетку в нужный цвет
        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return update_cells


screen = pygame.display.set_mode((800, 650))


#класс, для инициализации кнопки
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    #проверяет нажата ли кнопка и рисует ее
    def draw(self):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 640))

    # load button images
    run_img = pygame.image.load('run_button.png').convert_alpha()
    # create button instances
    run_button = Button(1, 601, run_img, 0.15)

    cells = np.zeros((60, 80))
    screen.fill(COLOR_GRID)
    update(screen, cells, 10)

    pygame.display.flip()
    pygame.display.update()

    running = False

    while True:
        #реализуем различные действия в зависимости от того какое действие происходит в окне
        for event in pygame.event.get():
            #игра закрыта
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            #нажата кнопка
            elif run_button.draw():
                running = not running
                update(screen, cells, 10)
                pygame.display.update()

            #нажата одна из ячеек
            if (pygame.mouse.get_pressed()[0]):
                pos = pygame.mouse.get_pos()
                if pos[1] <= 600:
                    cells[pos[1] // 10, pos[0] // 10] = 1
                update(screen, cells, 10)
                pygame.display.update()

        screen.fill(COLOR_GRID)

        if running:
            screen.blit(run_button.image, (run_button.rect.x, run_button.rect.y))
            cells = update(screen, cells, 10, with_progress=True)
            pygame.display.update()

        time.sleep(0.001)


if __name__ == '__main__':
    main()
