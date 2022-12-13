# Import the pygame module
import pygame
# Import random for random numbers
import random
import numpy as np
import leaderboard
#import scipy

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define constants for the screen width and height, global variables because reasons
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
#tuple to make life easier
SCREEN_CENTER = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
DIVIDER = SCREEN_WIDTH/2
#LEVEL is an int from 1,10
LEVEL = 1

#for updating colors, in progress
class Section():
    def __init__(self, screen):
        self.rect = pygame.draw.rect(screen,(255,0, 0),(200,150,100,50))





# Define the Particle object extending pygame's Sprite object
class Particle(pygame.sprite.Sprite):
    def __init__(self):
        super(Particle, self).__init__()
        self.surf = pygame.image.load("dn.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        # The starting position is randomly generated, as is the speed
        #self.x =
        #self.y = random.randint(0, SCREEN_HEIGHT)
        self.vx = random.randint(1,3)
        self.vy = random.randint(1,3)
        self.m = 1

        self.rect = self.surf.get_rect(
            center=(
                #set spread of particles based on game level difficulty
                random.randint(0, SCREEN_WIDTH/2 + int(SCREEN_WIDTH*LEVEL/10)),
                random.randint(0, SCREEN_HEIGHT),
            )
        )







    # Move the particle based on speed
    def update(self):

        # bounce particle on the edge screen
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.vy = -self.vy
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.vx = -self.vx


        self.rect.move_ip(self.vx, self.vy)

    def change_velocities(p1, p2):
        """
        Particles p1 and p2 have collided elastically: update their
        velocities. 'Self is p1, because it's easier to read that way

        """

        m1, m2 = p1.m, p2.m
        M = m1 + m2
        d = 2

        def change_vcoord(v1, v2):
            u1 = v1 - 2 * m2 / M * np.dot(v1 - v2, 2) / d * 2
            u2 = v2 - 2 * m1 / M * np.dot(v2 - v1, 2) / d * 2

            return u1, u2


        p1.vx, p2.vx = change_vcoord(p1.vx, p2.vx)
        p1.vy, p2.vy = change_vcoord(p1.vy, p2.vy)
        p1.update()
        p2.update()
    #checks location of particle



class Demon(Particle):
    def __init__(self):
        super(Demon, self).__init__()
        self.surf = pygame.image.load("sdevil.gif").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(SCREEN_CENTER))
        self.m = 1
        self.vx = 0
        self.vy = 0


    # Move the sprite based on keypresses
    def move(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            #move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            #move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep player on the screen
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.left <= 0:
            self.rect.left = 0
        elif self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def update(self):
        # bounce particle on the edge screen
        if self.rect.top <= 1 or self.rect.bottom >= SCREEN_HEIGHT -1:
            self.vy = -self.vy
        if self.rect.left <= 1 or self.rect.right >= SCREEN_WIDTH -1:
            self.vx = -self.vx
        self.rect.move_ip(self.vx, self.vy)


#




def startGame():
    # Setup for sounds
    pygame.mixer.init()
    # Initialize pygame
    pygame.init()
    # Setup the clock for a decent framerate
    clock = pygame.time.Clock()

    # Create the screen object
    # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maxwell Pong")
    #split the screen into left and right sides
    LHS = Section(screen)

    # create group for all sprites, used for rendering
    all_sprites = pygame.sprite.Group()
    # Create groups to hold particle sprites, used for collision detection and position updates
    all_particles = pygame.sprite.Group()
    #create a count for the number of particles on the left hand side of the screen
    lhs_particles = pygame.sprite.Group()
    # Create our 'player'
    demon = Demon()
    #add player to all sprites group
    all_sprites.add(demon)


    #create particles and add them to particle group
    for i in range(5):
        particle = Particle()
        if particle.rect.left <= DIVIDER:
            lhs_particles.add(particle)
            print(particle.rect.left)
        #checks if particle is on LHS of screen, if it is increase the count by one
        all_particles.add(particle)
        all_sprites.add(particle)



    running = True

    # Our main loop
    while running:

        # Look at every event in the queue

        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop
                if event.key == K_ESCAPE:
                    running = False

            # Did the user click the window close button? If so, stop the loop
            elif event.type == QUIT:
                running = False



        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()
        demon.move(pressed_keys)



        # Fill the screen with sky black
        screen.fill((0, 0, 0))

        #update each sprite
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)


        # check each particle
        for entity in all_particles:
            if entity.rect.left < DIVIDER:
                lhs_particles.add(entity)
            else:
                entity.remove(lhs_particles)
            print(len(lhs_particles))
            #if the particle makes contact with the demon sprite, reflect back
            if entity.rect.colliderect(demon.rect):
                entity.vx = -entity.vx
                entity.vy = -entity.vy
                entity.update()

            #make a list of collisions for this sprite
            collision_list = pygame.sprite.spritecollide(entity, all_particles, False)
            for c in collision_list:
                #update velocity for both sprites
                entity.change_velocities(c)


            #if more than half of the particles end up in the right hand side of the screen, the player has lost
            if len(lhs_particles) < len(all_particles)/2:
               running = False


        all_particles.update()
        pygame.display.set_caption("Maxwell Pong SCORE: "+ str(len(lhs_particles)))

        # Flip everything to the display
        pygame.display.flip()

        # Ensure we maintain a 30 frames per second rate
        clock.tick(5)

    # stop and quit the mixer
    pygame.mixer.music.stop()
    pygame.mixer.quit()




#define a main loop
def main():
    '''calls functions which open a game window and populate it with sprites'''
    startGame()

#if this is the main module, run the program
if __name__ == '__main__':
    main()