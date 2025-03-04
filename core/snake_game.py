import pygame
import random
import sys
import json
import math

class SnakeGame:
    """Classe pour la logique du jeu Snake"""
    def __init__(self, background_img):
        self.screen_width = 500
        self.screen_height = 500
        self.cell_size = 20
        self.background_img = pygame.transform.scale(background_img, (self.screen_width, self.screen_height))
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Snake II")
        self.clock = pygame.time.Clock()
        self.running = True
        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.direction = "RIGHT"
        self.food = self.spawn_food()
        self.score = 0
        # Initialisation des monstres
        self.monsters = []
        self.max_monsters = 3  # Nombre maximum de monstres à l'écran
        self.spawn_monster()  # Créer le premier monstre

    def spawn_food(self):
        """Fait apparaître un morceau de nourriture à une position aléatoire"""
        x = random.randint(0, (self.screen_width // self.cell_size) - 1) * self.cell_size
        y = random.randint(0, (self.screen_height // self.cell_size) - 1) * self.cell_size
        return [x, y]

    def spawn_monster(self):
        """Fait apparaître un monstre à une position aléatoire"""
        if len(self.monsters) < self.max_monsters:
            # S'assurer que le monstre n'apparaît pas sur le serpent ou sur la nourriture
            while True:
                x = random.randint(0, (self.screen_width // self.cell_size) - 1) * self.cell_size
                y = random.randint(0, (self.screen_height // self.cell_size) - 1) * self.cell_size
                monster_pos = [x, y]
                
                # Vérifier que le monstre n'apparaît pas sur le serpent ou la nourriture
                if monster_pos not in self.snake and monster_pos != self.food and monster_pos not in self.monsters:
                    self.monsters.append(monster_pos)
                    break

    def move_snake(self):
        """Déplace le serpent"""
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
            # Réinitialiser les monstres quand le fruit est mangé
            self.monsters = []
            self.spawn_monster()  # Faire apparaître un nouveau monstre
        else:
            self.snake.pop()

    def move_monsters(self):
        """Déplace les monstres vers la tête du serpent"""
        snake_head = self.snake[0]
        updated_monsters = []
        
        for monster in self.monsters:
            # Calculer la direction vers la tête du serpent
            dx = snake_head[0] - monster[0]
            dy = snake_head[1] - monster[1]
            
            # Normaliser la direction pour ne se déplacer que d'une cellule
            monster_move = monster[:]
            
            # Déplacement horizontal
            if abs(dx) > abs(dy):
                if dx > 0:
                    monster_move[0] += self.cell_size
                elif dx < 0:
                    monster_move[0] -= self.cell_size
            # Déplacement vertical
            else:
                if dy > 0:
                    monster_move[1] += self.cell_size
                elif dy < 0:
                    monster_move[1] -= self.cell_size
            
            # Vérifier que le monstre reste dans les limites
            if (0 <= monster_move[0] < self.screen_width and 
                0 <= monster_move[1] < self.screen_height):
                updated_monsters.append(monster_move)
            else:
                updated_monsters.append(monster)
                
        self.monsters = updated_monsters

    def check_collision(self):
        """Vérifie si le serpent est entré en collision avec un mur, lui-même ou un monstre"""
        head = self.snake[0]
        # Collision avec les murs
        if head[0] < 0 or head[0] >= self.screen_width or head[1] < 0 or head[1] >= self.screen_height:
            return True
        # Collision avec lui-même
        if head in self.snake[1:]:
            return True
        # Collision avec un monstre
        if head in self.monsters:
            return True
        return False

    def draw_elements(self):
        """Dessine les éléments du jeu"""
        self.screen.blit(self.background_img, (0, 0))
        
        # Dessiner le serpent
        for segment in self.snake:
            pygame.draw.rect(self.screen, (0, 255, 0), (*segment, self.cell_size, self.cell_size))
        
        # Dessiner la nourriture
        pygame.draw.rect(self.screen, (255, 0, 0), (*self.food, self.cell_size, self.cell_size))
        
        # Dessiner les monstres
        for monster in self.monsters:
            pygame.draw.rect(self.screen, (128, 0, 128), (*monster, self.cell_size, self.cell_size))
        
        # Afficher le score
        font = pygame.font.Font(None, 24)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        
        pygame.display.flip()

    def save_score(self):
        """Sauvegarde le score du joueur"""
        try:
            with open("data/scores.json", "r") as file:
                scores = json.load(file)
        except FileNotFoundError:
            scores = []

        scores.append(self.score)

        with open("data/scores.json", "w") as file:
            json.dump(scores, file)

    def run(self):
        """Lance le jeu"""
        monster_spawn_timer = 0
        monster_move_interval = 5  # Les monstres se déplacent tous les 5 cycles
        monster_spawn_interval = 50  # Un nouveau monstre apparaît tous les 50 cycles
        
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

            # Déplacer le serpent
            self.move_snake()
            
            # Gérer les monstres
            monster_spawn_timer += 1
            if monster_spawn_timer % monster_move_interval == 0:
                self.move_monsters()
            if monster_spawn_timer % monster_spawn_interval == 0:
                self.spawn_monster()
            
            # Vérifier les collisions
            if self.check_collision():
                self.save_score()
                print(f"Game Over! Your score: {self.score}")
                self.running = False
                
            self.draw_elements()
            self.clock.tick(10)
        pygame.quit()
        sys.exit()