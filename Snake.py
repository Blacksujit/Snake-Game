import pygame
from pygame.locals import *
import time
import random
import os

SIZE = 32

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("food.png")
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 30) * SIZE
        self.y = random.randint(1, 14) * SIZE

class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("Snakelogo.png")
        self.direction = 'down'
        self.length = length
        self.x = [32] * length
        self.y = [32] * length

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        self.parent_screen.blit(self.image, (self.x[0], self.y[0]))
        for i in range(1, self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


#  add the obstacle functionality in which the game play is enhanced such that if the snake coliide with the obstacle the ganme will be over 
class Obstacle:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        obstacle_images = [
            "tree.png",
            "fences.png",
            "water_puddle.png",
        ]
        self.image = pygame.image.load(random.choice(obstacle_images)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.x = random.randint(1, 30) * SIZE
        self.y = random.randint(1, 14) * SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        print("Current working directory:", os.getcwd())
        self.play_background_music()
        pygame.display.set_caption("Snake And Insect Game")
        self.surface = pygame.display.set_mode((1000, 500))
        self.snake = Snake(self.surface, 5)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.level = 1
        self.speed = 0.17
        self.obstacles = [Obstacle(self.surface) for _ in range(5)]
        
        

    def play_background_music(self):
        try:
            pygame.mixer.music.load('Random Tone.mp3')
            pygame.mixer.music.play(-1, 2)
        except pygame.error as e:
            print(f"Error loading background music: {e}")

    def play_sound(self, sound_name):
        try:
            if sound_name == "crash":
                sound = pygame.mixer.Sound("crash.mp3")
            elif sound_name == 'ding':
                sound = pygame.mixer.Sound("ding.mp3")

            pygame.mixer.Sound.play(sound)
        except pygame.error as e:
            print(f"Error playing sound {sound_name}: {e}")

    def reset(self):
        self.snake = Snake(self.surface, 5)
        self.apple = Apple(self.surface)
        self.obstacles = [Obstacle(self.surface) for _ in range(5)]
        self.level = 1
        self.speed = 0.17

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load("background.jpg")
        self.surface.blit(bg, (0, 0))
        for obstacle in self.obstacles:
            obstacle.draw()


#  score board is also added to dipslay the game at each level

#  thus the game level complexity will increase as the snake will eat the bug at each level
    def display_score_and_level(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length - 5}", True, (200, 200, 200))
        self.surface.blit(score, (850, 10))
        level = font.render(f"Level: {self.level}", True, (200, 200, 200))
        self.surface.blit(level, (850, 40))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length - 5}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def increase_level(self):
        self.level += 1
        self.speed = max(0.05, self.speed - 0.02)

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score_and_level()
        pygame.display.flip()

        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

            if (self.snake.length - 5) % 5 == 0:
                self.increase_level()
                self.obstacles.append(Obstacle(self.surface))

        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise Exception("Collision Occurred")

        for obstacle in self.obstacles:
            if self.is_collision(self.snake.x[0], self.snake.y[0], obstacle.x, obstacle.y):
                self.play_sound("crash")
                raise Exception("Collision with Obstacle")

        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 500):
            self.play_sound('crash')
            raise Exception("Hit the boundary error")

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(self.speed)

if __name__ == '__main__':
    game = Game()
    game.run()
