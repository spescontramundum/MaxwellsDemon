import unittest
from unittest import TestCase
import pygame
import pynput
import game
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


class TestStartGame(TestCase):
    def test_main(self):
        game.main()


class TestParticle(TestCase):
    '''tests automatic (non-user directed) movement for particles'''

    def test_update(self):
        pygame.init()
        screen = pygame.display.set_mode((game.SCREEN_WIDTH, game.SCREEN_HEIGHT))
        part = game.Particle()

        # attempt to move the sprites past the top of the window
        part.rect.top = 0
        part.rect.move_ip(0, -5)

        # check and see if the sprites are actually past the top of the window
        self.assertLess(part.rect.top, 0, "Particles cannot go past top of window")

        # attempt to move the sprites past the bottom of the window
        part.rect.bottom = game.SCREEN_HEIGHT
        part.rect.move_ip(0, 5)
        # if it allows the demon sprite past the edge of the screen the test fails
        self.assertLess(part.rect.top, game.SCREEN_HEIGHT)

    def test_change_velocities(self):
        self.fail()



class TestDemon(TestCase):

    def test_move(self):
        # create a controller to simulate keypresses
        kb = pynput.keyboard.Controller()

        pygame.init()
        screen = pygame.display.set_mode((game.SCREEN_WIDTH, game.SCREEN_HEIGHT))
        dem = game.Demon()
        #put the demon sprite at the top edge of the window
        dem.rect.top = 0
        #try to move it up, past the top
        dem.move(kb.press(pynput.keyboard.Key.up))
        kb.release(pynput.keyboard.Key.up)
        self.assertGreater(dem.rect.top, 0)


if __name__ == '__main__':
    unittest.main()
    print("Everything passed")

