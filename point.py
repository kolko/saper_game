#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os, sys
import pygame
from config import *
from pygame.locals import *

class Sprite(pygame.sprite.Sprite):
    " Base class for Sprite "
    def __init__(self, x = 0, y = 0):
        "Initialisation"
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y

    def move_x(self, x):
        self.x = self.x + x
        self._move()
    
    def move_y(self, y):
        self.y = self.y + y
        self._move()
        
    def set_x(self, x):
        self.x = x
        self._move()
    
    def set_y(self, y):
        self.y = y
        self._move()
        
    def _move(self):
        self.rect.center = (self.x,self.y)


    # Sprite image initialization
    def init_image(self, imgPath):
        self.image = pygame.image.load(imgPath).convert()
        self.image.set_colorkey(self.image.get_at((0,0)), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)

class TextSprite(Sprite):
    def __init__(self, x, y, text='', size=20, color=(0,0,255)):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, size)  # load the default font, size 25
        self.color = color         # our font color in rgb
        self.text = text
        #self.generateImage() # generate the image
 
    def setText(self, text):
        self.text = text
        if text == 'b':
            self.color = (255, 0, 0)
        elif text == 'f':
            self.color = (255, 150, 100)
        self.generateImage()
    def setColor(self, color):
        self.color = color
        self.generateImage()
    def setSize(self, size):
        self.font = pygame.font.Font(None, size)
        self.generateImage()
    
    def generateImage(self):
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

class Point(pygame.sprite.Sprite):
    def __init__(self, x, y, area, parent, bomb=False):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        #self.image, self.rect = load_image(img, -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.px = x
        self.py = y
        self.x = x*20
        self.y = y*20+40
        self.area_p = area
        self.bomb = bomb
        self.open = False #открыто
        self.flag = False #отмечен флагом
        self.textSprite = TextSprite(self.x+10,self.y+10)
        self.paint()
        self.generateImage()
        
    def generateImage(self):
        self.image = pygame.image.load(os.path.join('data', 'point.png')).convert()
        self.image.set_colorkey(self.image.get_at((0,0)), RLEACCEL)
        self.rect = self.image.get_rect()
        
        #self.rect = self.image.get_rect()
        self.rect.center = (self.x+10, self.y+10)
        #print 'genimage'
        
    def get_surface_rect(self):
        left = self.rect.left
        top = self.rect.top
        width = self.rect.width
        height = self.rect.height*0.1
        return pygame.Rect(left, top, width, height)
        
    def paint(self):
        if self.open:
            if self.have_bomb():
                self.textSprite.setText('b')
                self.parent.end_game(1)
            else:
                number = self.near_bombs()
                self.textSprite.setText('%d'%(number,))
                if number == 0:
                    self.textSprite.setText('-')
                    for p in self.get_around():
                        if p.open == False:
                            p.push()
        elif self.flag:
            self.textSprite.setText('f')
        else:
            self.textSprite.setText(' ')
        self.textSprite.generateImage()
        
    def _test_p(self, x, y):
        if x in range(len(self.area_p[0])):
            if y in range(len(self.area_p)):
                return True
        return False
        
    def have_bomb(self):
        if self.bomb:
            return True
        return False
        
    def get_around(self):
        ret = []
        if self._test_p(self.px-1, self.py-1):
            ret.append(self.area_p[self.px-1][self.py-1])
        if self._test_p(self.px, self.py-1):
            ret.append(self.area_p[self.px][self.py-1])
        if self._test_p(self.px+1, self.py-1):
            ret.append(self.area_p[self.px+1][self.py-1])
        if self._test_p(self.px-1, self.py):
            ret.append(self.area_p[self.px-1][self.py])
        if self._test_p(self.px+1, self.py):
            ret.append(self.area_p[self.px+1][self.py])
        if self._test_p(self.px-1, self.py+1):
            ret.append(self.area_p[self.px-1][self.py+1])
        if self._test_p(self.px, self.py+1):
            ret.append(self.area_p[self.px][self.py+1])
        if self._test_p(self.px+1, self.py+1):
            ret.append(self.area_p[self.px+1][self.py+1])
        return ret
        
    def near_bombs(self):
        b = 0
        for x in self.get_around():
            if x.have_bomb():
                b += 1
        return b
        
    def push(self):
        if not self.flag:
            self.open = True
        self.paint()
        #print 'Push!'
    
    def p_flag(self):
        if not self.open:
            self.flag = not self.flag
        self.paint()
        #print 'Flag!'
    
    def p_test(self):
        b = self.near_bombs()
        print b, self.open, self.flag
        if (b > 0) and (self.open) and (not self.flag):
            #print 'do test!'
            f_len = 0
            for x in self.get_around():
                if x.flag:
                    f_len += 1
            if f_len == b:
                for x in self.get_around():
                    x.push()
        #print 'Test!'