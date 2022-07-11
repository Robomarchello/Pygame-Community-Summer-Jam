import pygame
from pygame.locals import *
from random import choice


pygame.init()

class Button():
    def __init__(self, rect, text, font, rectColor, textColor, func):
        self.rect = rect
        self.text = text
        self.font = font
        self.rectColor = rectColor
        self.textColor = textColor
        self.func = func
        self.mp = pygame.Vector2(0, 0)
        self.onRect = False

    def draw(self, screen):
        textRender = self.font.render(self.text, False, self.textColor)
        textRect = textRender.get_rect()
        textRect.center = self.rect.center
        
        pygame.draw.rect(screen, self.rectColor, self.rect)
        screen.blit(textRender, textRect.topleft)

        if self.rect.collidepoint(self.mp):
            self.onRect = True
            #This was pretty cool though
            #pygame.mouse.set_cursor(SYSTEM_CURSOR_HAND)
        else:
            self.onRect = False
            #pygame.mouse.set_cursor(SYSTEM_CURSOR_ARROW)

    def handle_event(self, event):
        if event.type == MOUSEMOTION:
            self.mp = pygame.Vector2(event.pos) / 4
        
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.onRect:
                    self.func()


class RestartMenu():
    def __init__(self, rect, inactiveY, gameOver):
        self.rect = rect

        self.surface = pygame.Surface(self.rect.size)

        self.restart = False

        self.active = False
        self.activePos = pygame.Vector2(rect.copy().center[0], rect.copy().top)
        self.inactivePos = pygame.Vector2(rect.copy().center[0], inactiveY)
        self.animation = 0.0
        self.animationSpeed = 0.03

        self.gameOver = gameOver
        self.restartCounter = 0

        self.color = pygame.Color('grey')
        self.textColor = pygame.Color('darkgrey')
        self.buttonColor = pygame.Color('green')
        self.buttonTextColor = pygame.Color('darkgreen')

        self.titleText = pygame.font.Font('assets/font/font.ttf', 15)
        self.regularText = pygame.font.Font('assets/font/font.ttf', 8)

        self.GameOverStr = 'Game Over!'
        #load it from json file;) like "Give it another try!", "You can do better!", 
        self.randomStrings = ['Give it another try!', 'You can do better!',
        'You should try again;)', 'Restart and do better']

        self.randomStr = ''
        self.updateString()

        restartBtnRect = self.rect.copy()
        restartBtnRect.width = restartBtnRect.width * 0.8
        restartBtnRect.height = self.rect.height // 4
        restartBtnRect.center = self.rect.center
        restartBtnRect.bottom = self.rect.bottom - 10

        self.restartButton = Button(restartBtnRect, 'Restart', self.regularText,
        self.buttonColor, self.buttonTextColor, self.restartFunc)

    def restartFunc(self):
        '''
        Restarts the game and the gameOver menu,
        so you can restart multiple times
        '''
        
        self.restartCounter += 1
        self.restart = True
    
    def updateString(self):
        '''updates self.randomStr'''
        self.randomStr = choice(self.randomStrings)

    def draw(self, screen):
        if self.gameOver.GameOver:
            if self.animation < 1 - self.animationSpeed:
                self.animation += self.animationSpeed
                self.rect.top = self.inactivePos.lerp(self.activePos, self.animation)[1]
        
        else:
            if self.animation > self.animationSpeed:
                self.animation -= self.animationSpeed
                self.rect.top = self.inactivePos.lerp(self.activePos, self.animation)[1]
            
            else:
                self.gameOver.visible = False
                self.updateString()
                if self.restartCounter == 3:
                    self.randomStr = 'Fun fact: You died 3 times'

        pygame.draw.rect(screen, self.color, self.rect)
        
        GameOverText = self.titleText.render(self.GameOverStr, False, self.textColor)
        GameOverRect = GameOverText.get_rect()
        GameOverRect.center = self.rect.center
        GameOverRect.top = self.rect.top + 5
        screen.blit(GameOverText, GameOverRect)

        RandomText = self.regularText.render(self.randomStr, False, self.textColor)
        RandomTextRect = RandomText.get_rect()
        RandomTextRect.center = self.rect.center
        RandomTextRect.top = self.rect.top + 25
        screen.blit(RandomText, RandomTextRect)

        self.restartButton.rect.bottom = self.rect.bottom - 10

        self.restartButton.draw(screen)
    
    def handle_event(self, event):
        self.restartButton.handle_event(event)


class GameOver():
    def __init__(self, ScreenSize, screen):
        self.ScreenSize = ScreenSize
        
        self.RestartMenuRect = pygame.Rect(0, 0, 150, 100)
        self.RestartMenuRect.center = (ScreenSize[0] // 2, ScreenSize[1] // 2)
        self.RestartMenu = RestartMenu(self.RestartMenuRect, ScreenSize[1], self)

        self.visible = False
        self.GameOver = False

    #def updateGreySurf()

    def restart(self, HealthBar):
        if self.RestartMenu.restart:
            HealthBar.hp = HealthBar.rect.width / HealthBar.hpPerPixel
            self.RestartMenu.restart = False
            self.GameOver = False
            
    def draw(self, screen):
        if self.visible:# if gameover: is pretty bad way to do this😅
            self.RestartMenu.draw(screen)

    def handle_event(self, event):
        self.RestartMenu.handle_event(event)

