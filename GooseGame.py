'''
GOOSE GAME                      #change title later

By:
Karan Sharma 21023433
Alina XinLin Zhu 20999257
Ege Cagdas 21020905

Citations:

'''



## INITIALIZATION
import pygame, random, math, sys                            #import the different modules to be used

pygame.init()                                               #initialize pygame

pygame.mixer.pre_init(44100, -16, 2, 2048)                  #pre-initialize mixer, used to work with sound/music
pygame.mixer.init()                                         #initialize mixer, used to work with sound/music
pygame.mixer.music.load(".wav")                             #import the background music
pygame.mixer.music.play(-1)                                 #plays the backround music on loop

scared_sfx = pygame.mixer.Sound(".wav")                     #set variable for sound effect when humans get scared
game_over_sfx = pygame.mixer.Sound(".wav")                  #set variable for sound effect when you lose the game
level_passed_sfx = pygame.mixer.Sound(".wav")               #set variable for sound effect when you pass the level
congrats_sfx = pygame.mixer.Sound(".wav")                   #set variable for sound effect when you beat the game

white = [225,225,225]                                       #set variable for colour white
black = [0,0,0]                                             #set variable for colour black
colour = [225,225,225]                                      #set variable for colour 

font = pygame.font.Font(None, 40)                           #set font size and type

screen = pygame.display.set_mode([1500, 1000])              #Create new window for the game, with dimensions 1500x1000 pixels
pygame.display.set_caption("Goose Game")                    #Set the title for the game that appears on the new window

Sprites_list = pygame.sprite.Group()                        #create sprite group for all sprites
Game_over_list = pygame.sprite.Group()                      #create sprite group for sprites that cause a game over

clock = pygame.time.Clock()                                 #set variable for clock



## CLASSES FOR SPRITES AND BUTTONS
class Button():                                                                                                                     #class for the buttons used in menu screens
    def __init__(self, pos, text_input):                                                                                            #initialize class
        self.image = pygame.image.load("Button.png")                                                                                #import image for the button
        self.image = pygame.transform.scale(self.image, [200, 100])                                                                 #scale image to size of 200x100 pixels

        self.text_input = text_input                                                                                                #set variable for text displayed on button
        self.text = font.render(self.text_input, True, white)                                                                       #render text displayed on button to screen
        
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))                                                                  #initialiaze position of button, alligning center to specified position on screen
        self.text_rect = self.text.get_rect(center = (pos[0], pos[1]))                                                              #initialiaze position of text, alligning center to specified position on screen

    def update(self, mouse_pos):                                                                                                    #define function for when button updates itself in-game
        self.text = font.render(self.text_input, True, white)                                                                       #render text on screen

        if mouse_pos[0] in range(self.rect.left, self.rect.right) and mouse_pos[1] in range(self.rect.top, self.rect.bottom):       #check if mouse is hovering over the button image
            self.text = font.render(self.text_input, True, colour)                                                                  #render text on screen, but with different colour to indicate it can be pressed

        screen.blit(self.image, self.rect)                                                                                          #add the button, and it's position to the screen
        screen.blit(self.text, self.text_rect)                                                                                      #add the text, and it's position to the screen

    def check_input(self, mouse_pos):                                                                                               #define function to check if button has been pressed
        if mouse_pos[0] in range(self.rect.left, self.rect.right) and mouse_pos[1] in range(self.rect.top, self.rect.bottom):       #check if mouse is hovering over the button image
            return True                                                                                                                 #confirm that the button has been clicked
        return False                                                                                                                #confirm that the button has not been clicked


class Goose(pygame.sprite.Sprite):                                                                                                  #Class for the goose (playable character)
    def __init__(self):                                                                                                             #initialize class
        pygame.sprite.Sprite.__init__(self)                                                                                         #initialize itself as a sprite

        self.image = pygame.image.load(".png")                                                                                      #import image for the sprite
        self.image = pygame.transform.scale(self.image, [50, 50])                                                                   #scale image to size 50x50 pixels

        self.rect = self.image.get_rect()                                                                                           #initialize the position of the sprite
        self.rect.x = 725                                                                                                           #set variable of x position, with value of 725
        self.rect.y = 425                                                                                                           #set variable of x position, with value of 425

        self.score = 0                                                                                                              #set variable of goose's score, with value of 0 at start of game

    def update(self):                                                                                                               #define function for when sprite updates itself in-game
        keys = pygame.key.get_pressed()                                                                                             #initialize kets

        move = pygame.math.Vector2(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT], keys[pygame.K_DOWN] - keys[pygame.K_UP])             #set movement for goose as a 2-d vector using the input keys
        if move.length_squared() > 0:                                                                                               #check if the goose is moving by finding absolute value squared of movement vector
            move.scale_to_length(5)                                                                                                     #set movement to the speed = 5, by scaling the length (absolute value) to 5

            self.rect.x += round(move.x)                                                                                                #move goose on x-axis by the x component of movement vector
            self.rect.y += round(move.y)                                                                                                #move goose on y-axis by the y component of movement vector

        self.rect.clamp_ip(pygame.display.get_surface().get_rect())                                                                 #bound the goose within the size of the screen, so it doesn't travel out of sight
