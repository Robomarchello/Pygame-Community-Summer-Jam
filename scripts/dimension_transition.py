import pygame

pygame.init()


class TransCircle():
    def __init__(self, position, color, speed):
        self.position = position  
        self.color = color
        self.speed = speed 

        self.radius = 0
        self.maxRadius = 150
        self.width = 0
        self.maxWidth = 15
        
        self.dead = False

    def draw(self, screen):
        self.radius += self.speed
        if self.radius > self.maxRadius:
            self.dead = True

        if self.width < self.maxWidth:
            self.width += self.speed

        pygame.draw.circle(screen, self.color, self.position, self.radius, int(self.width))        


class dimTrans:
    def __init__(self, portalRect):
        self.portal_rect = portalRect
        
        self.change_scene = False
        self.change = False
        self.active = False

        self.speed = 1.5
        self.colorIndex = 0
        self.color = [pygame.Color(100, 0, 100), pygame.Color(50, 0, 50)]

        self.TransCircles = []
        
        self.circlesSpawned = 0
        self.maxCircles = 10

    def draw(self, screen):
        if self.active:
            for transCircle in self.TransCircles:
                transCircle.draw(screen)
                transCircle.position = self.portal_rect.center

                if transCircle.dead:
                    self.TransCircles.remove(transCircle)
            
            if not self.change:
                if self.TransCircles[-1].width >= self.TransCircles[-1].maxWidth:
                    self.TransCircles.append(TransCircle(self.portal_rect.center, self.color[self.colorIndex], self.speed))
                    
                    self.circlesSpawned += 1
                    self.colorIndex += 1
                    if self.colorIndex > 1:
                        self.colorIndex = 0

            if self.circlesSpawned > self.maxCircles:
                if not self.change:
                    self.change_scene = True
                self.change = True

            if len(self.TransCircles) == 0 and self.change:
                self.clear()
    
    def activize(self):
        self.active = True

        self.TransCircles.append(TransCircle(self.portal_rect.center, self.color[self.colorIndex], self.speed))
        self.colorIndex += 1
        if self.colorIndex > 1:
            self.colorIndex = 0

    def clear(self):
        self.TransCircles = []
        self.active = False
        self.change = False
        self.change_scene = False
        self.circlesSpawned = 0

#self.dimTrans = dimTrans(pygame.Rect(0, 0, 200, 150))
#            if self.dimTrans.change_scene:
#                screen.fill((255, 0, 0))
#
#            self.dimTrans.draw(screen)