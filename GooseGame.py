'''
The Goose Training Camp

By:
Karan Sharma 21023433
Alina XinLin Zhu 20999257
Ege Cagdas 21020905

Citations:

'''



## INITIALIZATION
import pygame, random, math, sys                                    #import the different modules to be used

pygame.init()                                                       #initialize pygame

pygame.mixer.pre_init(44100, -16, 2, 2048)                          #pre-initialize mixer, used to work with sound/music
pygame.mixer.init()                                                 #initialize mixer, used to work with sound/music

scared_sfx1 = pygame.mixer.Sound("Scream1.wav")                     #set variable 1 for sound effect when humans get scared
scared_sfx2 = pygame.mixer.Sound("Scream2.wav")                     #set variable 2 for sound effect when humans get scared
scared_sfx3 = pygame.mixer.Sound("Scream3.wav")                     #set variable 3 for sound effect when humans get scared
s_sfx_list = [scared_sfx1, scared_sfx2, scared_sfx3]                #set list of variables for sound effects when human get scared

pause_sfx = pygame.mixer.Sound("Quack.wav")                         #set variable for sound effect when you pause the level
button_hover_sfx = pygame.mixer.Sound("Swoosh.wav")                 #set variable for sound effect when you hover over a button
button_click_sfx = pygame.mixer.Sound("Click.wav")                  #set variable for sound effect when you click a button

white = [225, 225, 225]                                             #set variable for colour white
black = [0, 0, 0]                                                   #set variable for colour black
yellow = [225, 225, 0]                                              #set variable for colour yellow

title_font = pygame.font.Font("Sketching Universe.otf", 70)         #set font size and type for the title
button_font = pygame.font.Font("Party Confetti.ttf", 30)            #set font size and type for the buttons
text_font = pygame.font.Font("Milk Kids.otf", 30)                   #set font size and type for the text

screen = pygame.display.set_mode([1500, 1000])                      #Create new window for the game, with dimensions 1500x1000 pixels
pygame.display.set_caption("The Goose Training Camp")               #Set the title for the game that appears on the new window

Sprites_list = pygame.sprite.Group()                                #create sprite group for all sprites
Game_over_list = pygame.sprite.Group()                              #create sprite group for sprites that cause a game over

clock = pygame.time.Clock()                                         #set variable for clock



## CLASSES FOR SPRITES AND BUTTONS
class Button():                                                                                                                         #class for the buttons used in menu screens
    def __init__(self, pos, text_input):                                                                                                    #initialize class, based on mouse position and text to be displayed
        self.image = pygame.image.load("Button.png")                                                                                            #import image for the button
        self.image = pygame.transform.scale(self.image, [220, 80])                                                                              #scale image to size of 200x80 pixels

        self.text_input = text_input                                                                                                            #set variable for text displayed on button
        self.text = button_font.render(self.text_input, True, white)                                                                            #render text displayed on button to screen
        
        self.rect = self.image.get_rect(center = (pos[0], pos[1]))                                                                              #initialiaze position of button, alligning center to specified position on screen
        self.text_rect = self.text.get_rect(center = (pos[0], pos[1]))                                                                          #initialiaze position of text, alligning center to specified position on screen

        self.hover = False                                                                                                                      #initialize variable that indicates if mouse hovered over button as false

    def update(self, mouse_pos):                                                                                                            #define function for when button updates itself in-game
        self.text = button_font.render(self.text_input, True, white)                                                                            #render text on screen

        if mouse_pos[0] in range(self.rect.left, self.rect.right) and mouse_pos[1] in range(self.rect.top, self.rect.bottom):                   #check if mouse is hovering over the button image
            self.text = button_font.render(self.text_input, True, yellow)                                                                           #render text on screen, but now yellow to indicate it can be pressed

            if not self.hover:                                                                                                                      #check if button has not been hovered over
                pygame.mixer.Sound.play(button_hover_sfx)                                                                                               #play button hover sound to indicate it can be pressed
                self.hover = True                                                                                                                       #set variable to indicate button has been hovered over
        
        else:                                                                                                                                   #continue if button is not being hovered over
            self.hover = False                                                                                                                      #set variable as false

        screen.blit(self.image, self.rect)                                                                                                      #add the button, and it's position to the screen
        screen.blit(self.text, self.text_rect)                                                                                                  #add the text, and it's position to the screen

    def check_input(self, mouse_pos):                                                                                                       #define function to check if button has been pressed
        if mouse_pos[0] in range(self.rect.left, self.rect.right) and mouse_pos[1] in range(self.rect.top, self.rect.bottom):                   #check if mouse is hovering over the button image
            pygame.mixer.Sound.play(button_click_sfx)                                                                                               #play sound effect to indicate button has been clicked

            return True                                                                                                                             #confirm that the button has been clicked

        return False                                                                                                                            #confirm that the button has not been clicked


class Goose(pygame.sprite.Sprite):                                                                                              #class for the goose (playable character)
    def __init__(self):                                                                                                             #initialize class
        pygame.sprite.Sprite.__init__(self)                                                                                             #initialize itself as a sprite

        self.image = pygame.image.load(".png")                                                                                          #import image for the sprite
        self.image = pygame.transform.scale(self.image, [50, 50])                                                                       #scale image to size 50x50 pixels

        self.rect = self.image.get_rect()                                                                                               #initialize the position of the sprite
        self.rect.x = 725                                                                                                               #set variable of x position, with value of 725
        self.rect.y = 425                                                                                                               #set variable of x position, with value of 425

        self.score = 0                                                                                                                  #set variable of goose's score, with value of 0 at start of game

    def update(self):                                                                                                               #define function for when sprite updates itself in-game
        keys = pygame.key.get_pressed()                                                                                                 #initialize kets

        move = pygame.math.Vector2(keys[pygame.K_RIGHT] - keys[pygame.K_LEFT], keys[pygame.K_DOWN] - keys[pygame.K_UP])                 #set movement for goose as a 2-d vector using the input keys
        if move.length_squared() > 0:                                                                                                   #check if the goose is moving by finding absolute value squared of movement vector
            move.scale_to_length(5)                                                                                                         #set movement to the speed = 5, by scaling the length (absolute value) to 5

            self.rect.x += round(move.x)                                                                                                    #move goose on x-axis by the x component of movement vector
            self.rect.y += round(move.y)                                                                                                    #move goose on y-axis by the y component of movement vector

        self.rect.clamp_ip(pygame.display.get_surface().get_rect())                                                                     #bound the goose within the size of the screen, so it doesn't travel out of sight


class Human(pygame.sprite.Sprite):                                                                                          #class for the human (enemy)
    def __init__(self, GS):                                                                                                     #initialize class
        pygame.sprite.Sprite.__init__(self)                                                                                         #initialize itself as a sprite

        self.image = pygame.image.load(".png")                                                                                      #import image for the sprite
        self.image = pygame.transform.scale(self.image, [50, 50])                                                                   #scale image to size 50x50 pixels

        self.rect = self.image.get_rect()                                                                                           #initialize the position of the sprite
        self.start_axis = random.randrange(1, 3)                                                                                    #determine which axis to spawn human

        self.scared = False                                                                                                         #set variable for scared condition to false
        self.GS = GS                                                                                                                #set variable for class goose

        '''
        Explanation for path generation:
        1. Determine random starting position of human, either: top, bottom, left, or right side of screen
        2. Determine the random speed of human, which bassically determine direction
        3. Code designed in a way so that they will always travel across the screen
        4. Code designed in a way so that they will travel further forward, and less to the sides
            - This is there to make it more likely for the path of the human to intercept the nest
            - 2nd reason is that it prevents humans from traveling very short paths on the corners
        '''

        if self.start_axis == 1:                                                                                                    #check if human starts on x-axis
            self.rect.x = random.randrange(-50, 1500)                                                                                   #pick a random value on the x-axis to start on
            self.rect.y = random.choice([-50, 1000])                                                                                    #choose whether to start on top or bottom of screen

            self.x_speed = random.randrange(-3, 4)                                                                                      #set speed on x-axis as random value from -3 to 3

            self.y_speed = random.randrange(3, 6)                                                                                       #if on the top, set speed on y-axis as random value from 3 to 5 (so it moves down)
            if self.rect.y == 1000:                                                                                                     #check if on the bottom
                self.y_speed = random.randrange(-5, -2)                                                                                     #set speed on y_axis as random value from -5 to -3 (so it moves up)

        else:                                                                                                                       #human starts on y_axis
            self.rect.x = random.choice([-50, 1500])                                                                                    #choose whether to start on left or right of screen
            self.rect.y = random.randrange(-50, 1000)                                                                                   #pick a random value on the y-axis to start on

            self.x_speed = random.randrange(3, 6)                                                                                       #if on the left, set speed on x-axis as random value from 3 to 5 (so it moves right)
            if self.rect.x == 1500:                                                                                                     #check if on the right
                self.x_speed = random.randrange(-5, -2)                                                                                     #set speed on x_axis as random value from -5 to -3 (so it moves up)

            self.y_speed = random.randrange(-3, 4)                                                                                      #set speed on y-axis as random value from -3 to 3
    
    def update(self):                                                                                                           #define function for when sprite updates itself in-game
        self.rect.x += self.x_speed                                                                                                 #update x position based on speed on x_axis
        self.rect.y += self.y_speed                                                                                                 #update y position based on speed on y_axis

        self.x_distance = (self.GS.rect.x + 25) - (self.rect.x + 25)                                                                #calculate disatance on x between goose and human (x component)
        self.y_distance = (self.GS.rect.y + 25) - (self.rect.y + 25)                                                                #calculate disatance on y between goose and human (y component)
        distance_goose = math.sqrt((self.x_distance)**2 + (self.y_distance)**2)                                                     #calculate actual distance based off x and y components

        if distance_goose <= 120 and not self.scared:                                                                               #check if goose closer than 120 pixels and human is not scared
            self.x_speed = -self.x_distance/12                                                                                          #set x speed of human as opposite of distance to goose (so it is running away)
            self.y_speed = -self.y_distance/12                                                                                          #set y speed of human as opposite of distance to goose (so it is running away)

            self.scared = True                                                                                                          #make itself scared (so goose cant scare it again)

            pygame.mixer.Sound.play(random.choice(s_sfx_list))                                                                          #play random sound effect from list to indicate human is scared
        
        if self.scared:                                                                                                             #check if human is scared
            if self.rect.left <= -50 or self.rect.right > 1550 or self.rect.top <= -50 or self.rect.bottom > 1050:                      #check if human crosses border of screen (playing area)
                self.GS.score += 1                                                                                                          #increase score of goose by 1

                Sprites_list.remove(self)                                                                                                   #remove itself from the game by removing itself from the list of sprites
        
        distance_nest = math.sqrt((self.rect.x - 725)**2 + (self.rect.y - 475)**2)                                                  #calculate distance of human to the nest (distance to center of screen)

        if distance_nest <= 100:                                                                                                    #check if nest is closer than 100 pixels
            Game_over_list.add(self)                                                                                                    #add human to game_over_list, to indicate the condition has been met for the game to end


class Nest(pygame.sprite.Sprite):                                           #class for nest (area to protect)
    def __init__(self):                                                         #initialize class
        pygame.sprite.Sprite.__init__(self)                                         #initialize itself as a sprite

        self.image = pygame.image.load(".png")                                      #import image for the sprite
        self.image = pygame.transform.scale(self.image, [50, 50])                   #scale image to size 50x50 pixels

        self.rect = self.image.get_rect()                                           #initialize the position of the sprite
        self.rect.x = 725                                                           #set variable of x position, with value of 725         
        self.rect.y = 475                                                           #set variable of x position, with value of 475
    
    def update(self):                                                           #define function for when sprite updates itself in-game
        pass                                                                        #do nothing



##INFORMATION SCREENS
def main_menu(current_level, music):                                                #function for the main menu screen, based off current level and music status
    quit_b = Button([495, 600], "Quit")                                                 #create button the exit the game
    play_b = Button([750, 600], "Play")                                                 #create button to play the game
    instructions_b = Button([1005,600], "Instructions")                                 #create button to read the instructions

    image = pygame.image.load("Background.jpg")                                         #import the backround image
    bg = pygame.transform.scale(image, [1500, 1000])                                    #scale backround image to 1500x1000

    if music:                                                                           #if music is set to restart (= True)
        pygame.mixer.music.load("Menu.wav")                                                 #load in the music
        pygame.mixer.music.play(-1)                                                         #play the music on loop

    while True:                                                                         #continue running screen until a button is pressed
        screen.blit(bg, (0, 0))                                                             #add backround to the screen

        mouse_pos = pygame.mouse.get_pos()                                                  #get the position of the mouse

        pygame.draw.rect(screen, black, pygame.Rect(345, 295, 810, 410))                    #draw black rectangle on screen with dimensions 810x410, centered in middle
        pygame.draw.rect(screen, white, pygame.Rect(350, 300, 800, 400))                    #draw white rectangle on screen with dimensions 800x400, centered in middle

        title = title_font.render("The Goose Training Camp", True, black)                   #create text for the title, colour is black
        title_rect = title.get_rect(center = (750, 400))                                    #determine position of the title, center it on (750, 100)
        screen.blit(title, title_rect)                                                      #add the title to the screen

        for b in [play_b, instructions_b, quit_b]:                                          #run code for every button created
            b.update(mouse_pos)                                                                 #update the button to check if mouse is hovering over it
        
        for event in pygame.event.get():                                                    #run code for every new event in the game
            if event.type == pygame.QUIT:                                                       #check if player presses the X on the window bar
                pygame.quit()                                                                       #quite the game
                sys.exit()                                                                          #exit the system

            if event.type == pygame.MOUSEBUTTONDOWN:                                            #check if player clicked with their mouse
                if play_b.check_input(mouse_pos):                                                   #check if player clicked the play button
                    if current_level == 6:                                                              #check if player is beaten all levels
                        congrats()                                                                          #go to the congrats screen

                    level_info(current_level, False)                                                    #go to the level info screen, dont restart the music

                if instructions_b.check_input(mouse_pos):                                           #check if player clicked the instructions button
                    instructions(current_level)                                                         #go to the instructions screen

                if quit_b.check_input(mouse_pos):                                                   #check if player clicked the quit button
                    pygame.quit()                                                                       #quite the game
                    sys.exit()                                                                          #exit the system
        
        clock.tick(60)                                                                      #update the screen 60 times per second (fps)
        pygame.display.update()                                                             #update the display


def instructions(current_level):                                                    #function for the instructions screen, based off current level    
    text_list = ["You are a Goose",                                                     #create list of text to be used
        "Control your character sing the arrow keys",
        "Your objective is to protect your nest, by scaring away humans",
        "Get close enough to a human to scare them away",
        "If the humans get too close to your nest, you lose",
        "To pass, scare away 10 humans before the time runs out",
        "Beat all 5 levels to become a certified goose",
        "Now go get those pesky humans",]

    exit_b = Button([750, 730], "Exit")                                                 #set button for exiting the screen

    while True:                                                                         #continue running screen until exited
        mouse_pos = pygame.mouse.get_pos()                                                  #get position of the mouse

        pygame.draw.rect(screen, black, pygame.Rect(320, 195, 860, 610))                    #draw black rectangle on screen with dimensions 860x610, centered in middle
        pygame.draw.rect(screen, white, pygame.Rect(325, 200, 850, 600))                    #draw white rectangle on screen with dimensions 850x600, centered in middle

        text = title_font.render("How to Play", True, black)                                #create text for the title of the screen, set colour to black
        text_rect = text.get_rect(center = (750, 250))                                      #get position of the title, center on (750, 100)
        screen.blit(text, text_rect)                                                        #add text to the screen

        t_pos = 340                                                                         #set position of the text as 340
        for t in text_list:                                                                     #run code for every line of text to be added
            text = text_font.render(t, True, black)                                             #create text of that line, set colour to black
            text_rect = text.get_rect(center = (750, t_pos))                                    #get position of text, place on vertical center and position value given
            screen.blit(text, text_rect)                                                        #add the text to the screen

            t_pos += 40                                                                         #increase the position value for the next line by 40

        exit_b.update(mouse_pos)                                                            #update the exit button to check if being hovered over
        
        for event in pygame.event.get():                                                    #run code for every new event in game
            if event.type == pygame.QUIT:                                                       #check if player presses the X on the window bar
                pygame.quit()                                                                       #quit pygame
                sys.exit()                                                                          #exit the system
            
            if event.type == pygame.MOUSEBUTTONDOWN:                                            #check if player clicked with their mouse
                if exit_b.check_input(mouse_pos):                                                   #check if player clicked on the exit button
                    main_menu(current_level, False)                                                     #go to main menu screen, dont restart the music

        clock.tick(60)                                                                      #update the screen 60 times per second (fps)
        pygame.display.update()                                                             #update the display


def level_info(current_level, music):                                                                               #function for level info screen, based off curent level and music status
    text_list = [["Level 1", "You have 70 seconds to scare away 10 humans", "Human speed is set to slow"],              #list of text to be used, position linked to current level
    ["Level 2", "You have 60 seconds to scare away 10 humans"],
    ["Level 3", "You have 50 seconds to scare away 10 humans"],
    ["Level 4", "You have 40 seconds to scare away 10 humans"],
    ["Level 5", "You have 30 seconds to scare away 10 humans"]]

    menu_b = Button([550, 600], "Menu")                                                                                 #set button to return to main menu
    next_b = Button([950, 600], "Next")                                                                                 #set button to play the game

    image = pygame.image.load("Background.jpg")                                                                         #import a backround image
    bg = pygame.transform.scale(image, [1500, 1000])                                                                    #scale backround image to 1500x1000

    if music:                                                                                                           #check if music is set to restart (= True)
        pygame.mixer.music.load("Menu.wav")                                                                                 #load in the music
        pygame.mixer.music.play(-1)                                                                                         #play the music on loop

    while True:                                                                                                         #run code until a button is pressed
        screen.blit(bg, (0, 0))                                                                                             #add backround to the screen

        mouse_pos = pygame.mouse.get_pos()                                                                                  #get position of mouse

        pygame.draw.rect(screen, black, pygame.Rect(345, 295, 810, 410))                                                    #draw black rectangle on screen with dimensions 810x410, centered in middle
        pygame.draw.rect(screen, white, pygame.Rect(350, 300, 800, 400))                                                    #draw white rectangle on screen with dimensions 800x400, centered in middle 
        
        t_pos = 390                                                                                                         #set initial position for the text as 390
        for t in text_list[current_level - 1]:                                                                              #run code for every line of text in corresponding level
            text = text_font.render(t, True, black)                                                                             #create text of the line, colour is black
            text_rect = text.get_rect(center = (750, t_pos))                                                                    #get position of text, centered vertically and set to text position given
            screen.blit(text, text_rect)                                                                                        #add text to the screen
            
            t_pos += 40                                                                                                         #increase the position value for the next line by 40

        for b in [next_b, menu_b]:                                                                                          #run loop for every button created
            b.update(mouse_pos)                                                                                                 #update button
        
        for event in pygame.event.get():                                                                                    #run code for every event in game
            if event.type == pygame.QUIT:                                                                                       #check if player presses the X on the window bar
                pygame.quit()                                                                                                       #quit pygame
                sys.exit()                                                                                                          #exit the system

            if event.type == pygame.MOUSEBUTTONDOWN:                                                                            #check if player clicked with their mouse
                if next_b.check_input(mouse_pos):                                                                                   #check if player clicked the next button
                    play(current_level, True)                                                                                           #go the play screen, restart the music

                if menu_b.check_input(mouse_pos):                                                                                   #check if player clicked the menu button
                    main_menu(current_level, False)                                                                                     #go to main meny screen, dont restart the music

        clock.tick(60)                                                                                                      #update the screen 60 times per second (fps)
        pygame.display.update()                                                                                             #update the display



##GAMEPLAY SCREENS
def play(current_level, music):                                                                     #function to run the game screen based off current level an music status
    Sprites_list.empty()                                                                                #empty the sprites list as its a new level
    Game_over_list.empty()                                                                              #empty the game over list as its a new level

    NS = Nest()                                                                                         #create variable of the nest class
    Sprites_list.add(NS)                                                                                #add nest variable to sprites list

    GS = Goose()                                                                                        #create variable of the goose class
    Sprites_list.add(GS)                                                                                #add goose variable to sprites list

    time = [70, 60, 50, 40, 30]                                                                         #set list of the timer values, position corresponding to level

    level_pass = False                                                                                  #set condition for level passed as False
    lose = False                                                                                        #set condition for game lost as False
    tick = 0                                                                                            #set tick as 0 for the timer

    image = pygame.image.load("Park.png")                                                               #import a backround image
    bg = pygame.transform.scale(image, [1500, 1000])                                                    #scale backround image to 1500x1000

    if music:                                                                                           #check if music is set to restart (= True)
        pygame.mixer.music.load("Gameplay.wav")                                                             #load in the music
        pygame.mixer.music.play(-1)                                                                         #play the music on loop

    while not level_pass and not lose:                                                                  #continue loop while level has not been passed and game is not over
        screen.blit(bg, (0, 0))                                                                             #add backround to the screen

        tick += 1                                                                                           #increase tick by 1
        if tick % 60 == 0:                                                                                  #check if tick == 60 (1 second has passed)
            time[current_level - 1] -= 1                                                                        #decrease the current timer by 1 second

        if tick % 90 == 0:                                                                                  #check if tick == 90 (1.5 second has passed)
            HM = Human(GS)                                                                                      #create varaible for human class
            Sprites_list.add(HM)                                                                                #add human variable to sprites list

        timer = text_font.render("Timer = " + str(time[current_level - 1]), True, black)                    #render the timer, with text colour black
        screen.blit(timer, [10, 10])                                                                        #add the timer on to the screen at position (10, 10)

        score = text_font.render("Humans left = " + str(10 - GS.score), True, black)                        #render the score, with text colour black
        screen.blit(score, [10, 50])                                                                        #add the score on to the screen at position (10, 50)

        Sprites_list.update()                                                                               #update all the sprites in sprites list
        Sprites_list.draw(screen)                                                                           #draw all the sprites in sprites list to the screen

        for event in pygame.event.get():                                                                    #run code for every new event in the game
            if event.type == pygame.QUIT:                                                                       #check if player presses the X on the window bar
                pygame.quit()                                                                                       #quite the game
                sys.exit()                                                                                          #exit the system

            if time[current_level - 1] <= 0 or len(Game_over_list.sprites()) > 0:                               #check if timer has reached 0, or human has gotten near the nest
                humans_left = 10 - GS.score                                                                         #count how many humans remained to beat the level

                GS.score = 0                                                                                        #reset score to 0

                lose = True                                                                                         #set lose condition to True

            if GS.score >= 10:                                                                                  #check if level has been beaten
                GS.score = 0                                                                                        #reset score to 0 

                level_pass = True                                                                                   #set win condition to True

            if event.type == pygame.KEYDOWN:                                                                    #check if player pressed a key on the keyboard
                if event.key == pygame.K_ESCAPE:                                                                    #check if key pressed was escape key
                    pygame.mixer.music.pause()                                                                          #pause the current music

                    pause(current_level)                                                                                #go to the pause screen

        clock.tick(60)                                                                                      #update the screen 60 times per second (fps)
        pygame.display.update()                                                                             #update the display
    
    if lose:                                                                                            #check if player lost the game
        you_lose(current_level, humans_left, time[current_level - 1])                                       #go to the game over screen, along with level stats

    if level_pass:                                                                                      #check if player passed the level
        level_passed(current_level + 1)                                                                     #go to the level passed screen, and increase current level by 1


def pause(current_level):                                                           #function to pause the game, based off curent level
    restart_b = Button([610, 520], "Restart")                                           #set button for restarting level
    continue_b = Button([890, 520], "Continue")                                         #set button for exiting pause screen
    menu_b = Button([750, 630], "Menu")                                                 #set button for returning to main menu

    pygame.mixer.Sound.play(pause_sfx)                                                  #play sound effect to indicate level is paused

    paused = True                                                                       #set paused variable as true
    while paused:                                                                       #continue while game still paused
        mouse_pos = pygame.mouse.get_pos()                                                  #get position of the mouse

        pygame.draw.rect(screen, black, pygame.Rect(445, 295, 610, 410))                    #draw black rectangle on screen with dimensions 610x410, centered in middle
        pygame.draw.rect(screen, white, pygame.Rect(450, 300, 600, 400))                    #draw white rectangle on screen with dimensions 600x400, centered in middle
        
        text = title_font.render("Game Paused", True, black)                                #create text for the pause screen title
        text_rect = text.get_rect(center = (750, 380))                                      #get position for the text, center on (750, 250)
        screen.blit(text, text_rect)                                                        #add text to screen

        for b in [restart_b, continue_b, menu_b]:                                           #run loop for every button created
            b.update(mouse_pos)                                                                 #update button to check if being hovered over
        
        for event in pygame.event.get():                                                    #run code for every new event in the game
            if event.type == pygame.QUIT:                                                       #check if player presses the X on the window bar
                pygame.quit()                                                                       #quit pygame
                sys.exit()                                                                          #exit the system
            
            if event.type == pygame.MOUSEBUTTONDOWN:                                            #check if players has clicked with their mouse
                if restart_b.check_input(mouse_pos):                                                #check if player clicked restart button
                    play(current_level, True)                                                           #go to the play screen
                
                if continue_b.check_input(mouse_pos):                                               #check if player has clicked the continue button
                    pygame.mixer.music.unpause()                                                        #unpaue the music

                    paused = False                                                                      #exit the loop and return back to the play function
                
                if menu_b.check_input(mouse_pos):                                                   #check if player has clicked the menu button
                    main_menu(current_level, True)                                                      #go to the meny screen

        clock.tick(60)                                                                      #update the screen 60 times per second (fps)
        pygame.display.update()                                                             #update the display



##AFTER GAME SCREENS
def level_passed(current_level):                                                    #function for screen when player beats a level, based off current level
    next_b = Button([600, 600], "Next")                                                #set button to continue to next level
    menu_b = Button([900, 600], "Menu")                                                 #set button to return to main meny

    image = pygame.image.load("Background.jpg")                                         #import a backround image
    bg = pygame.transform.scale(image, [1500, 1000])                                    #scale backround image to 1500x1000

    pygame.mixer.music.load("Victory.wav")                                              #load in the music
    pygame.mixer.music.play(1)                                                         #play the music on loop

    while True:                                                                         #continue running code until button is pressed
        screen.blit(bg, (0, 0))                                                             #add backround to the screen
        
        mouse_pos = pygame.mouse.get_pos()                                                  #get the position of the mouse

        pygame.draw.rect(screen, black, pygame.Rect(445, 295, 610, 410))                    #draw black rectangle on screen with dimensions 810x410, centered in middle
        pygame.draw.rect(screen, white, pygame.Rect(450, 300, 600, 400))                    #draw white rectangle on screen with dimensions 600x600, centered in middle
        
        text = title_font.render("Level Passed", True, black)                               #create text for the title of the screen, colour is black
        text_rect = text.get_rect(center = (750, 400))                                      #set position for the text, center on (750, 400)
        screen.blit(text, text_rect)                                                        #add text to the screen

        for b in [next_b, menu_b]:                                                          #run code for every button created
            b.update(mouse_pos)                                                                 #update button to check if being hovered over
        
        for event in pygame.event.get():                                                    #run code for every event in game
            if event.type == pygame.QUIT:                                                       #check if player presses the X on the window bar
                pygame.quit()                                                                       #exit pygame
                sys.exit()                                                                          #exit the system

            if event.type == pygame.MOUSEBUTTONDOWN:                                            #check if player has clicked with their mouse
                if next_b.check_input(mouse_pos):                                                   #check if player clicked the next button
                    if current_level == 6:                                                              #check if player has passed all levels
                        congrats()                                                                          #go to the congrats screen

                    level_info(current_level, True)                                                     #go to the level info screen

                if menu_b.check_input(mouse_pos):                                                   #check if player clicked the menu button
                    main_menu(current_level, True)                                                      #go to the main menu screen

        clock.tick(60)                                                                      #update the screen 60 times per second (fps)
        pygame.display.update()                                                             #update the display


def you_lose(current_level, humans_left, time_left):                                        #function for screen when you lose a level, based off curent level, number of humans left, and time left
    menu_b = Button([600, 630], "Menu")                                                         #set button to return to menu screen
    retry_b = Button([900, 630], "Retry")                                                       #set button to retry the level

    image = pygame.image.load("Background.jpg")                                                 #import a backround image
    bg = pygame.transform.scale(image, [1500, 1000])                                            #scale backround image to 1500x1000

    pygame.mixer.music.load("Sad.wav")                                                          #load in the music
    pygame.mixer.music.play(1)                                                                  #play the music on loop

    while True:                                                                                 #run code until button has been pressed
        screen.blit(bg, (0, 0))                                                                     #add backround to the screen

        mouse_pos = pygame.mouse.get_pos()                                                          #get position of the mouse

        pygame.draw.rect(screen, black, pygame.Rect(445, 295, 610, 410))                            #draw black rectangle on screen with dimensions 810x410, centered in middle
        pygame.draw.rect(screen, white, pygame.Rect(450, 300, 600, 400))                            #draw white rectangle on screen with dimensions 600x600, centered in middle
        
        text = title_font.render("Game Over", True, black)                                          #create text for the title of the screen, colour is black
        text_rect = text.get_rect(center = (750, 360))                                              #get position of the text, center on (750, 100)
        screen.blit(text, text_rect)                                                                #add text to the screen

        text_list = ["Level reached: ", "Humans left: ", "Time Remaining: "]                        #create list of text to add
        stats_list = [current_level, humans_left, time_left]                                        #set stats corresponding to position of text

        t_pos = 440                                                                                 #initialize position of text
        for i in range(3):                                                                          #run code for every line of text
            text = text_font.render(text_list[i] + str(stats_list[i]), True, black)                     #create text based of line and corresponding stat, colour is black
            text_rect = text.get_rect(center = (750, t_pos))                                            #get position of text, centered vertically and corresponding the position value
            screen.blit(text, text_rect)                                                                #add text to the screen
            
            t_pos += 40                                                                                 #increase position of next text line by 50

        for b in [retry_b, menu_b]:                                                                 #run code for every button created
            b.update(mouse_pos)                                                                         #update button
        
        for event in pygame.event.get():                                                            #run code for every event in game
            if event.type == pygame.QUIT:                                                               #check if player presses the X on the window bar
                pygame.quit()                                                                               #quit pygame
                sys.exit()                                                                                  #exit the system

            if event.type == pygame.MOUSEBUTTONDOWN:                                                    #check if player clicked with their mouse
                if menu_b.check_input(mouse_pos):                                                           #check if player clicked the menu button
                    main_menu(current_level, True)                                                              #go to the main menu screen, restart music

                if retry_b.check_input(mouse_pos):                                                          #check if player clicked the retry button
                    play(current_level, True)                                                                   #go to the play screen, restart music

        clock.tick(60)                                                                              #update the screen 60 times per second (fps)
        pygame.display.update()                                                                     #update the display


def congrats():                                                                         #function for screen when player beats all 5 levels
    menu_b = Button([750, 620], "Menu")                                                     #set button to return to main meny

    image = pygame.image.load("Background.jpg")                                             #import a backround image
    bg = pygame.transform.scale(image, [1500, 1000])                                        #scale backround image to 1500x1000

    pygame.mixer.music.load("Axel F.wav")                                                    #load in the music
    pygame.mixer.music.play(-1)                                                             #play the music on loop

    while True:                                                                             #continue running code until button is pressed
        screen.blit(bg, (0, 0))                                                                 #add backround to the screen

        mouse_pos = pygame.mouse.get_pos()                                                      #get the position of the mouse

        pygame.draw.rect(screen, black, pygame.Rect(445, 295, 610, 410))                        #draw black rectangle on screen with dimensions 810x410, centered in middle
        pygame.draw.rect(screen, white, pygame.Rect(450, 300, 600, 400))                        #draw white rectangle on screen with dimensions 600x600, centered in middle
        
        text = title_font.render("Congratulations", True, black)                                #create text for the title of the screen, colour is black
        text_rect = text.get_rect(center = (750, 360))                                          #get position of the text, center on (750, 400)
        screen.blit(text, text_rect)                                                            #add text to the screen

        text = text_font.render("You are now a certified goose", True, black)                   #create text
        text_rect = text.get_rect(center = (750, 480))                                          #get position of the text, center on (750, 500)
        screen.blit(text, text_rect)                                                            #add text on screen

        menu_b.update(mouse_pos)                                                                #update meny button
        
        for event in pygame.event.get():                                                        #run code for every event in game
            if event.type == pygame.QUIT:                                                           #check if player presses the X on the window bar
                pygame.quit()                                                                           #quit pygame
                sys.exit()                                                                              #exit the system

            if event.type == pygame.MOUSEBUTTONDOWN:                                                #check if player has clicked with their mouse
                if menu_b.check_input(mouse_pos):                                                       #check if player pressed the menu button
                    main_menu(1, True)                                                                      #go to main meny screen, restart music

        clock.tick(60)                                                                          #update the screen 60 times per second (fps)
        pygame.display.update()                                                                 #update the display



##RUN THE CODE TO PLAY
main_menu(1, True)              #run main menu function, with current level set to 1 and music set to restart