#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
import sys
from random import randint
from point import *
from config import *
import datetime

# Base class for location
class Location(object):
    parent = None
    def __init__(self, parent):
        self.window = pygame.display.get_surface()
        self.parent = parent
        self.background = pygame.image.load('data/background.png').convert()
    def event(self,event):
        pass
    def draw(self):
        pass


# first menu location
class StartLocation(Location):
    
    def __init__(self, parent):
        Location.__init__(self, parent)
        pygame.mouse.set_visible(1)
        pygame.key.set_repeat(0)
        self.messages = pygame.sprite.Group()
        self.window = pygame.display.get_surface()
        self.parent = parent
        self.restartbtn = TextSprite(40,15,'Restart',30,(0,0,0))
        self.mainbuttons = pygame.sprite.Group()
        self.restartbtn.generateImage()
        self.mainbuttons.add(self.restartbtn)
        #self.exitbtn = Button(240, 270, "Exit")
        #self.controls = pygame.sprite.Group()
        #self.surfaces = []
        #self.controls_captions = pygame.sprite.Group()
        #self.controls_captions.add(self.startbtn.textSprite)
        #self.controls_captions.add(self.exitbtn.textSprite)
        #self.controls.add(self.startbtn)
        #self.controls.add(self.exitbtn)
        self.window.blit(self.background, (0, 0))
        self.in_game = False
        self.restart()
        
    def draw(self):
        self.controls.clear(self.window, self.background)
        self.controls.draw(self.window)
        self.controls_captions.draw(self.window)
        self.mainbuttons.draw(self.window)
        self.messages.draw(self.window)
    
    def event(self,event):
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            sys.exit(0)
        else:
            pass
        if event.type == MOUSEBUTTONUP:
            for p in self.points:
                for point in p:
                    if (point.rect.collidepoint(pygame.mouse.get_pos())) and (self.in_game):
                    #pass
                        print event
                        if event.button == 1:
                            point.push()
                        elif event.button == 3:
                            point.p_flag()
                        elif event.button == 2:
                            point.p_test()
            x, y = pygame.mouse.get_pos()
            print 'x=%d,y=%d' % (x,y)
            self.test_finish()
            if y<40:
                self.restart()
                
#    def showInput(self):
#        self.input_surf = Rectangle(300, 100, (0,191,255,200))
#        self.surfaces.append(self.input_surf)   

    def bombing(self, points):
        #points[1][1].bomb = True
        for x in range(length_bomb):
            while True:
                x_p = randint(0, width_x-1)
                y_p = randint(0, height_y-1)
                if not points[x_p][y_p].bomb:
                    points[x_p][y_p].bomb = True
                    break
        return points
        
    def restart(self):
        self.controls = pygame.sprite.Group()
        self.messages = pygame.sprite.Group()
        self.controls_captions = pygame.sprite.Group()
        self.points = []
        for x in range(width_x):
            self.points.append([])
            for y in range(height_y):
                self.points[x].append(Point(x,y, self.points, self))
                
        for x in range(width_x):
            for y in range(height_y):
                self.points[x][y].paint()
                self.controls.add(self.points[x][y])
                self.controls_captions.add(self.points[x][y].textSprite)
        self.bombing(self.points)
        self.in_game = True
        self.st_time = datetime.datetime.now() 
        
    def end_game(self, reason):
        #reason 0 - win, 1 - fail
        self.in_game = False
        if reason == 1:
            for x in range(width_x):
                for y in range(height_y):
                     pass
                     #self.points[x][y].push()
        if reason == 0:
            message = TextSprite(width_x*20/2,height_y*20/2,'Winner!',50,(255,0,255))
            
        else:
            message = TextSprite(width_x*20/2,height_y*20/2,'Fail!',50,(255,0,0))
        message.generateImage()
        self.messages.add(message)
        
        
    def test_finish(self):
        finish = True
        for x in range(width_x):
            for y in range(height_y):
                if (self.points[x][y].bomb == False) and (self.points[x][y].open == False):
                    finish = False
        if finish:
            self.end_game(0)
            
            