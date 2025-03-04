import pygame
import random
import sys
import json

class SnakeGame:
    """Classe pour la logique du jeu Snake"""
    def __init__(self):
        self.screen_width = 500
        self.screen_height = 900
        self.cell_size = 20
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Snake II")
        self.clock = pygame.time.Clock()
        self.running = True
        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.direction = "RIGHT"
        self.food = self.spawn_food()
        self.score = 0
        self.monsters = []
        self.color_monsters = []
        self.count_monster = len(self.monsters)
        self.max_monsters = 10
        self.spawn_monster()
        self.background_pattern = self.generate_background_pattern()

    def generate_background_pattern(self):
        pattern = []
        for y in range(0, self.screen_height, self.cell_size):
            row = []
            for x in range(0, self.screen_width, self.cell_size):
                color = (0, random.randint(50, 100), 0)  # Vert foncé pixelisé
                row.append(color)
            pattern.append(row)
        return pattern

    def spawn_food(self):
        x = random.randint(0, (self.screen_width // self.cell_size) - 1) * self.cell_size
        y = random.randint(0, (self.screen_height // self.cell_size) - 1) * self.cell_size
        return [x, y]

    def spawn_monster(self):
        if len(self.monsters) < self.max_monsters:
            while True:
                x = random.randint(0, (self.screen_width // self.cell_size) - 1) * self.cell_size
                y = random.randint(0, (self.screen_height // self.cell_size) - 1) * self.cell_size
                monster_pos = [x, y]
                if monster_pos not in self.snake and monster_pos != self.food and monster_pos not in self.monsters:
                    self.monsters.append(monster_pos)
                    is_color_find = False
                    while not is_color_find:
                        # Random yellow 
                        color = (random.randint(200, 255), random.randint(200, 255), 0)
                        if color not in self.color_monsters:
                            is_color_find = True

                    self.color_monsters.append(color)
                    break

    def move_snake(self):
        head = self.snake[0][:]
        if self.direction == "UP":
            head[1] -= self.cell_size
        elif self.direction == "DOWN":
            head[1] += self.cell_size
        elif self.direction == "LEFT":
            head[0] -= self.cell_size
        elif self.direction == "RIGHT":
            head[0] += self.cell_size
        self.snake.insert(0, head)
        if head == self.food:
            self.food = self.spawn_food()
            self.score += 1
            if self.score % 2 == 0:
                self.spawn_monster()
        else:
            self.snake.pop()

    def move_monsters(self):
        """Déplace les monstres vers la tête du serpent"""
        snake_head = self.snake[0]
        updated_monsters = []
                
        for monster in self.monsters:
            dx = snake_head[0] - monster[0]
            dy = snake_head[1] - monster[1]
            
            monster_move = monster[:]
            
            if abs(dx) > abs(dy):
                if dx > 0:
                    monster_move[0] += self.cell_size
                elif dx < 0:
                    monster_move[0] -= self.cell_size
            else:
                if dy > 0:
                    monster_move[1] += self.cell_size
                elif dy < 0:
                    monster_move[1] -= self.cell_size
            
            if (0 <= monster_move[0] < self.screen_width and 
                0 <= monster_move[1] < self.screen_height):
                updated_monsters.append(monster_move)
            else:
                updated_monsters.append(monster)
                
        self.monsters = updated_monsters

    def check_collision(self):
        head = self.snake[0]
        if head[0] < 0 or head[0] >= self.screen_width or head[1] < 0 or head[1] >= self.screen_height:
            return True
        if head in self.snake[1:]:
            return True
        if head in self.monsters:
            return True
        return False

    def draw_snake(self):
        """Dessine le serpent avec un dégradé et une bordure."""
        for i, segment in enumerate(self.snake):
            # Dégradé de vert clair à foncé pour chaque segment
            color = (0, 255 - (i * 15), 0)
            pygame.draw.rect(self.screen, color, (*segment, self.cell_size, self.cell_size))

    def draw_elements(self):
        for y, row in enumerate(self.background_pattern):
            for x, color in enumerate(row):
                pygame.draw.rect(self.screen, color, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

        self.draw_snake()

        pygame.draw.rect(self.screen, (255, 0, 0), (*self.food, self.cell_size, self.cell_size))
        for monster, color in zip(self.monsters, self.color_monsters):
            pygame.draw.rect(self.screen, color, (*monster, self.cell_size, self.cell_size))
        
        font = pygame.font.Font(None, 24)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        pygame.display.flip()

    def run(self):
        monster_move_timer = 0
        monster_move_interval = 10  # Déplacement des monstres tous les 10 cycles
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.direction != "DOWN":
                        self.direction = "UP"
                    elif event.key == pygame.K_DOWN and self.direction != "UP":
                        self.direction = "DOWN"
                    elif event.key == pygame.K_LEFT and self.direction != "RIGHT":
                        self.direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                        self.direction = "RIGHT"
            self.move_snake()

            monster_move_timer += 1
            if monster_move_timer % monster_move_interval == 0:
                self.move_monsters()
            if self.check_collision():
                print(f"Game Over! Your score: {self.score}")
                self.running = False
            self.draw_elements()
            self.clock.tick(10)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    pygame.init()
    game = SnakeGame()
    game.run()
