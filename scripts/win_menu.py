import pygame
from pygame.locals import *
from random import choice
from .game_over import Button

pygame.init()


class WinMenu():
    def __init__(self, rect, inactiveY, EndManager):
        self.rect = rect

        self.surface = pygame.Surface(self.rect.size)

        self.restart = False

        self.active = False
        self.activePos = pygame.Vector2(rect.copy().center[0], rect.copy().top)
        self.inactivePos = pygame.Vector2(rect.copy().center[0], inactiveY)
        self.animation = 0.0
        self.animationSpeed = 0.03

        self.EndManager = EndManager

        self.color = pygame.Color('grey')
        self.textColor = pygame.Color('darkgrey')
        self.buttonColor = pygame.Color('red')
        self.buttonTextColor = pygame.Color('darkred')

        self.titleText = pygame.font.Font('assets/font/font.ttf', 12)
        self.regularText = pygame.font.Font('assets/font/font.ttf', 8)

        self.TitleStr = 'Congratulations!'

        self.description = 'You just won the game!'

        AgainBtnRect = self.rect.copy()
        AgainBtnRect.width = AgainBtnRect.width * 0.8
        AgainBtnRect.height = self.rect.height // 4
        AgainBtnRect.center = self.rect.center
        AgainBtnRect.bottom = self.rect.bottom - 10

        self.exitButton = Button(AgainBtnRect, 'Exit?', self.regularText,
        self.buttonColor, self.buttonTextColor, self.ExitFunc)

    def ExitFunc(self):
        pygame.quit()
        raise SystemExit

    def draw(self, screen):
        if self.EndManager.won:
            if self.animation < 1 - self.animationSpeed:
                self.animation += self.animationSpeed
                self.rect.top = self.inactivePos.lerp(self.activePos, self.animation)[1]
        
        else:
            if self.animation > self.animationSpeed:
                self.animation -= self.animationSpeed
                self.rect.top = self.inactivePos.lerp(self.activePos, self.animation)[1]
            
            else:
                self.EndManager.visible = False

        pygame.draw.rect(screen, self.color, self.rect)
        
        Title = self.titleText.render(self.TitleStr, False, self.textColor)
        TitleRect = Title.get_rect()
        TitleRect.center = self.rect.center
        TitleRect.top = self.rect.top + 5
        screen.blit(Title, TitleRect.topleft)

        Description = self.regularText.render(self.description, False, self.textColor)
        DescriptionRect = Description.get_rect()
        DescriptionRect.center = self.rect.center
        DescriptionRect.top = self.rect.top + 26
        screen.blit(Description, DescriptionRect.topleft)

        self.exitButton.rect.bottom = self.rect.bottom - 10

        self.exitButton.draw(screen)
    
    def handle_event(self, event):
        self.exitButton.handle_event(event)


class EndManager():
    def __init__(self, ScreenSize, screen):
        self.ScreenSize = ScreenSize
        
        self.winMenuRect = pygame.Rect(0, 0, 150, 100)
        self.winMenuRect.center = (ScreenSize[0] // 2, ScreenSize[1] // 2)
        self.winMenu = WinMenu(self.winMenuRect, ScreenSize[1], self)

        self.visible = False
        self.won = False

    def restart(self, HealthBar, game):
        if self.winMenu.restart:
            HealthBar.hp = HealthBar.rect.width / HealthBar.hpPerPixel
            self.winMenu.restart = False
            self.won = False
            game.player.hp = 100
            
    def draw(self, screen, dimension, game):
        if self.visible:
            self.winMenu.draw(screen)
        
        if dimension >= 3 and game.enemies[-1].health <= 0:
            self.won = True
            self.visible = True

    def handle_event(self, event):
        self.winMenu.handle_event(event)

