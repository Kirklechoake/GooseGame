import pygame
import math
import random

pygame.init()

black = [0,0,0] #sets black color

pygame.mixer.pre_init(4410, -16, 2 2048)
pygame.mixer.init()
pygame.mixer.music.load("")                                             #imports the song
pygame.mixer.music.play(-1)                                             #plays the song

sfx1 = pygame.mixer.Sound("")                                           #Sad sound effect

image = pygame.image.load("Park.png")                                   #Importing background image
size = [1500, 1000]                                                     #Size of the backround
bg = pygame.transform.scale(image, size)                                #Scaling the background image

font = pygame.font.Font(None, 40)                                       #Font size and type
screen = pygame.display.set_mode(size)                                  #Gameplay region
pygame.display.set_caption("")                                          #Game Title

class Goose(pygame.sprite.Sprite):
    def __init__(self, size, human_count):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("")                              #Imporint image for sprite
        self.size = [50, 50]
        self.image = pygame.transform.scale(self.image, self.size)
        self.rect = self.image.get_rect()
        self.rect.x = (size[0] - self.size[0])/2
        self.rect.y = (size[1] - self.size[1])/2 - self.size[1]         #starting position of sprite
        self.speed = 4
        self.score = human_count

    def update(self)
        keys = pygame.key.get_pressed()

        if self.rect.x > 0 and self.rect.x < 1420:                      #movement on x axis
            if keys[pygame.K_LEFT]
                self.rect.x -= self.speed
            if keys[pygame.K_RIGTHT]
                self.rect.x += self.speed
        elif self.rect.x <= 0:
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
        else:
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed

        if self.rect.y > 0 and self.rect.y < 920:                       #movement on y axis
            if keys[pygame.K_UP]:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN]:
                self.rect.y += self.speed
        elif self.rect.y <= 0:
            if keys[pygame.K_DOWN]:
                self.rect.y += self.speed
        else:
            if keys[pygame.K_UP]:
                self.rect.y -= self.speed
