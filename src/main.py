import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.SysFont("airal",25)

class Direction(Enum):
    RIGTH = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x , y')

#rgb colors
WHITE = (255,255,255)
RED = (200,0,0 )
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)
BLACK = (0,0,0)


BLOCK_SIZE =20
SPEED = 15

class SnakeGame:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # inti display
        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        # init game state
        self.direction = Direction.RIGTH

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x -BLOCK_SIZE, self.head.y),
                      Point(self.head.x -(2*BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0,(self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self._place_food()


    def _update_ui(self):
        self.display.fill(BLACK)
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x,pt.y,BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2 , pygame.Rect(pt.x+4 , pt.y + 4 , 12 ,12))

        pygame.draw.rect(self.display, RED , pygame.Rect(self.food.x,self.food.y, BLOCK_SIZE,BLOCK_SIZE))

        text = font.render("Score: " + str(self.score) , True, WHITE)
        self.display.blit(text, [0,0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGTH:
            x += BLOCK_SIZE
        if direction == Direction.LEFT:
            x -= BLOCK_SIZE
        if direction == Direction.DOWN:
            y += BLOCK_SIZE
        if direction == Direction.UP:
            y -= BLOCK_SIZE
        self.head = Point(x,y)

    def _is_collision(self):
        #hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0 :
            return False
        # eats itself
        if self.head in self.snake[1:]:
            return True

    def _to_other_side(self):
        if self.head.x == 0 - BLOCK_SIZE:
            self.head = Point(self.w,self.head.y)
            return
        if self.head.x == self.w :
            self.head = Point(0- BLOCK_SIZE,self.head.y)

        if self.head.y == 0 - BLOCK_SIZE:
            self.head = Point(self.head.x,self.h)
            return
        if self.head.y == self.h:
            self.head = Point(self.head.x,0- BLOCK_SIZE)

    def play_step(self):
        # 1. Collect User Input

        for event in pygame.event.get():
            if event == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                if event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGTH
                if event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
                if event.key == pygame.K_UP:
                    self.direction = Direction.UP

        # 2. Move
        self._move(self.direction)
        self.snake.insert(0,self.head)

        # 3. check game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 3.1 to bounce to other side
        self._to_other_side()


        # 4. place food
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. retuurn game over and score

        return game_over, self.score


if __name__ == "__main__":
    game = SnakeGame()

    while True:
        game_over, score  = game.play_step()
        if game_over == True:
             break

    print("Final Score :" , score)

    pygame.quit()
