
import pygame, sys, time, random, json, math
from pygame.locals import *


pygame.init()
WIDTH, HEIGHT = 1000, 600
surface=pygame.display.set_mode((WIDTH, HEIGHT),0,32)
fps=64
ft=pygame.time.Clock()
pygame.display.set_caption("Flappy Bird")


bird_image = pygame.image.load("bird.png")
bird_image = pygame.transform.scale(bird_image, (50, 50))



class Bird:
    def __init__(self):
        self.size = 50
        self.color = (0, 250, 30)
        self.y = HEIGHT//2
        self.x = 50
        self.gravity = 1.5
        self.target = None
        self.up_speed = 5
        self.target_height = 30
    def fall(self):
        self.y += self.gravity
    def move(self):
        if self.target is not None:
            if self.y>self.target:
                self.y -= self.up_speed
            else:
                self.target = None
    def set_target(self):
        self.target = self.y-self.target_height

class Pillar:
    def __init__(self, x):
        self.x = x
        top_range = (100, 300)
        self.gap = random.randint(150, 300)
        self.top_height = random.randint(top_range[0], top_range[1])

class Pillars:
    def __init__(self):
        self.pillars = []
        self.width = 100
        self.color = (180, 100, 30)
        self.colliding_color = (255, 30, 30)
        self.min_gap_between_pillars = 400
        self.speed = 4
        self.create_initial_pillars()
    def create_initial_pillars(self):
        min_x = WIDTH
        max_x = WIDTH+2000
        x = min_x
        while x<max_x:
            new_pillar = Pillar(x)
            self.pillars.append(new_pillar)
            x += self.width + self.min_gap_between_pillars
    def manage_all(self):
        new_pillars = []
        counts_to_be_removed = 0
        last_x = 0
        for index in range(len(self.pillars)):
            if self.pillars[index].x<(0-self.width):
                counts_to_be_removed += 1
            else:
                new_pillars.append(self.pillars[index])
                if self.pillars[index].x>last_x:
                    last_x = self.pillars[index].x
        last_x += self.min_gap_between_pillars
        for _ in range(counts_to_be_removed):
            new_pillar = Pillar(last_x)
            new_pillars.append(new_pillar)
            last_x += self.min_gap_between_pillars
        self.pillars = new_pillars[:]
    def move_all(self):
        for index in range(len(self.pillars)):
            self.pillars[index].x -= self.speed
    def check_collision(self, bird):
        for index in range(len(self.pillars)):
            pillar_x1 = self.pillars[index].x
            pillar_x2 = pillar_x1+self.width
            if pillar_x1<=(bird.x-(bird.size//2))<=pillar_x2 or pillar_x1<=(bird.x+(bird.size//2))<=pillar_x2:
                bird_y1 = bird.y-(bird.size//2)
                bird_y2 = bird.y+(bird.size//2)
                if bird_y1<=(self.pillars[index].top_height) or bird_y2>=(self.pillars[index].top_height+self.pillars[index].gap):
                    return True
        return False


class App:
    def __init__(self, surface):
        self.surface = surface
        self.play = True
        self.mouse=pygame.mouse.get_pos()
        self.click=pygame.mouse.get_pressed()
        self.color = {
            "sky": (40, 140, 180)
        }
        self.bird = Bird()
        self.pillars = Pillars()
        self.life = 3
        self.colliding = False
    def draw_bird(self):
        pygame.draw.circle(self.surface, self.bird.color, (self.bird.x, self.bird.y), self.bird.size//2)
        x1 = self.bird.x-(self.bird.size//2)
        y1 = self.bird.y-(self.bird.size//2)
        self.surface.blit(bird_image, (x1, y1))
    def draw_pillars(self):
        for index in range(len(self.pillars.pillars)):
            color = self.pillars.color
            if index==0 and self.colliding:
                color = self.pillars.colliding_color
            x = self.pillars.pillars[index].x
            top_y = 0
            top_height = self.pillars.pillars[index].top_height
            pygame.draw.rect(self.surface, color, (x, top_y, self.pillars.width, top_height))
            bottom_y = top_height+self.pillars.pillars[index].gap
            bottom_height = HEIGHT-bottom_y
            pygame.draw.rect(self.surface, color, (x, bottom_y, self.pillars.width, bottom_height))
    def manage_collision(self):
        if self.pillars.check_collision(self.bird):
            self.colliding = True
        else:
            self.colliding = False
    def render(self):
        self.draw_bird()
        self.draw_pillars()
    def action(self):
        self.manage_collision()
        self.bird.fall()
        self.bird.move()
        self.pillars.move_all()
        self.pillars.manage_all()
    def run(self):
        while self.play:
            self.surface.fill(self.color["sky"])
            self.mouse=pygame.mouse.get_pos()
            self.click=pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==KEYDOWN:
                    if event.key==K_TAB:
                        self.play=False
                    elif event.key==K_SPACE:
                        self.bird.set_target()
            #--------------------------------------------------------------
            self.render()
            self.action()
            # -------------------------------------------------------------
            pygame.display.update()
            ft.tick(fps)



if  __name__ == "__main__":
    app = App(surface)
    app.run()

