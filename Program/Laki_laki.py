import pygame
import os
import random
import sys
import json
from button import Button
from run import get_font
from main import main_menu

pygame.init()

judul = " HindarMania"


pygame.display.set_caption(judul)


pygame.mixer.music.load("Assets/Music/backsound.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()
pygame.mixer.music.play(-1)

FPS = 30

# Asset
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUN = [pygame.image.load(os.path.join("Assets/Design", "Laki_laki1.png")).convert_alpha(),
       pygame.image.load(os.path.join("Assets/Design", "Laki_laki2.png")).convert_alpha()]

JUMP = pygame.image.load(os.path.join("Assets/Design", "Laki_laki1.png")).convert_alpha()

DUCK = [pygame.image.load(os.path.join("Assets/Design", "Laki_laki_duck1.png")).convert_alpha(),
        pygame.image.load(os.path.join("Assets/Design", "Laki_laki_duck2.png")).convert_alpha()]

DRUM_BERGERAK = pygame.image.load(os.path.join("Assets/Design", "drum_gerak.png")).convert_alpha()

DRUM_DIAM = pygame.image.load(os.path.join("Assets/Design", "drum_diam.png")).convert_alpha()

PESAWAT = pygame.image.load(os.path.join("Assets/Design", "pesawat.png")).convert_alpha()

FONT = pygame.font.Font(os.path.join("Assets/Other",'PressStart2P-Regular.ttf'), 20)

BG = pygame.image.load(os.path.join("Assets/Design", "bg.png"))

MENU = pygame.image.load(os.path.join("Assets/Design", "menu.png"))

class KarakterLaki_laki:
    k_jump_value = 8

    def __init__(self):
        self.duck_img = DUCK
        self.run_img = RUN
        self.jump_img = JUMP

        self.Laki_laki_duck = False
        self.Laki_laki_run = True
        self.Laki_laki_jump = False

        self.step_index = 0
        self.jump_vel = self.k_jump_value
        self.image = self.run_img[0]
        self.k_rect = self.image.get_rect()
        self.k_rect.x = 80
        self.k_rect.y = 390
        self.k_jump_sound = pygame.mixer.Sound(os.path.abspath('Assets/Music/jump.mp3'))
        self.k_duck_sound = pygame.mixer.Sound(os.path.abspath('Assets/Music/duck.mp3'))
        self.gravity = 2

    def update(self, userInput):
        if (userInput[pygame.K_UP] or userInput[pygame.K_SPACE]) and not self.Laki_laki_jump:
            self.Laki_laki_duck = False
            self.Laki_laki_run = False
            self.Laki_laki_jump = True
            self.k_jump_sound.play()
        elif userInput[pygame.K_DOWN] and not self.Laki_laki_jump:
            self.Laki_laki_duck = True
            self.Laki_laki_run = False
            self.Laki_laki_jump = False
            self.k_duck_sound.play()
            self.k_duck_sound.set_volume(0.4)
        elif not (self.Laki_laki_jump or userInput[pygame.K_DOWN]):
            self.Laki_laki_duck = False
            self.Laki_laki_run = True
            self.Laki_laki_jump = False

        if self.Laki_laki_duck:
            self.duck()
        elif self.Laki_laki_run:
            self.run()
        elif self.Laki_laki_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0
            
    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.k_rect = self.image.get_rect()
        self.k_rect.x = 80
        self.k_rect.y = 410
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.k_rect = self.image.get_rect()
        self.k_rect.x = 80
        self.k_rect.y = 390
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.Laki_laki_jump:
            self.k_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.k_jump_value:
            self.Laki_laki_jump = False
            self.jump_vel = self.k_jump_value

        if self.k_rect.y < 390:
            self.k_rect.y += self.gravity

        if self.k_rect.y >= 390:
            self.k_rect.y = 390

    def draw_hitbox(self, SCREEN):
        SCREEN.blit(self.image, (self.k_rect.x, self.k_rect.y))
        # pygame.draw.rect(SCREEN, (255, 0, 0), self.k_rect, 2)

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw_hitbox(self, SCREEN):
        SCREEN.blit(self.image, self.rect)
        # pygame.draw.rect(SCREEN, (255, 0, 0), self.rect, 2)


class Drum_Bergerak(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 445
    def update(self):
        self.rect.x -= game_speed * 2  
        if self.rect.x < -self.rect.width:
            obstacles.pop()


class Drum_Diam(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 420


class Pesawat(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 350
        self.index = 0

    def draw_hitbox(self, SCREEN):
        # pygame.draw.rect(SCREEN, (255, 0, 0), self.rect, 2)
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image, self.rect)
        self.index += 1

def load_highscore():
    try:
        with open("highscore.json", "r") as file:
            data = json.load(file)
            if isinstance(data, dict):
                return data.get("highscore", 0)
            else:
                return 0
    except (FileNotFoundError, json.JSONDecodeError):
        return 0

def save_highscore(highscore):
    with open("highscore.json", "w") as file:
        json.dump({"highscore": highscore}, file)

highscore = load_highscore()

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, highscore
    run = True
    clock = pygame.time.Clock()
    Laki_laki = KarakterLaki_laki()
    # balon_udara_property = BalonUdara()  # Dihapus
    # airship_property = Airship()          # Dihapus
    game_speed = 15
    x_pos_bg = 0
    y_pos_bg = 0
    points = 0
    obstacles = []
    death_count = 0
    
    highscore = load_highscore()

    def score():
        global points, game_speed, highscore
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = FONT.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (950, 40)
        SCREEN.blit(text, textRect)


        if points > highscore: 
            highscore = points
            save_highscore(highscore)

        highscore_text = FONT.render("Highscore: " + str(highscore), True, (0, 0, 0))
        highscore_rect = highscore_text.get_rect()
        highscore_rect.center = (950, 80)
        SCREEN.blit(highscore_text, highscore_rect)
    
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        userInput = pygame.key.get_pressed()

        background()

        Laki_laki.draw_hitbox(SCREEN)
        Laki_laki.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(Drum_Bergerak(DRUM_BERGERAK))
            elif random.randint(0, 2) == 1:
                obstacles.append(Drum_Diam(DRUM_DIAM))
            elif random.randint(0, 2) == 2:
                obstacles.append(Pesawat(PESAWAT))

        for obstacle in obstacles:
            obstacle.draw_hitbox(SCREEN)
            obstacle.update()
            if Laki_laki.k_rect.colliderect(obstacle.rect):
                pygame.time.delay(2000)
                death_count += 1
                menu(death_count)

        # baris berikut dihapus karena sudah tidak ada objek tersebut
        # balon_udara_property.draw_hitbox(SCREEN)
        # balon_udara_property.update(game_speed)

        # airship_property.draw_hitbox(SCREEN)
        # airship_property.update(game_speed)

        score()

        clock.tick(FPS)
        pygame.display.update()

        # if death_count > 0:
        #     run = False

def menu(death_count):
    global points, highscore
    run = True
    while run:
        if death_count == 0:
            SCREEN.blit(MENU,(0, 0))
            text = FONT.render("Press any Key to Start", True, ("White"))
        elif death_count > 0:
            bg = pygame.image.load(os.path.join("Assets/Design", "menu.png"))
            SCREEN.blit(bg, (0, 0))
            text = FONT.render("Press any Key to Restart", True, ("White"))
            score = FONT.render("Your Score: " + str(points), True, ("White"))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
            highscore_text = FONT.render("Highscore: " + str(highscore), True, ("White"))
            highscore_rect = highscore_text.get_rect()
            highscore_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
            SCREEN.blit(highscore_text, highscore_rect)

        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                main()

if __name__ == "__main__":
    menu(death_count=0)
