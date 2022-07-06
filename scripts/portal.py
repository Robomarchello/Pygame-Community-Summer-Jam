import pygame
from random import randint


class Particle:
    def __init__(self, position, distance):
        self.position = position
        self.distance = distance
        self.angle = randint(0, 360)

        self.dead = False

    def draw(self, screen):
        if self.distance < 0:
            self.dead = True
        self.distance -= 0.5

        radius = self.distance // 4
        position = pygame.Vector2(0,0)
        position.from_polar((self.distance, self.angle))
        position += self.position

        pygame.draw.circle(screen, (255, 255, 255), position, radius)


class Portal():
    def __init__(self, position):
        self.elipseRect = pygame.Rect(10, 0, 33, 52)

        self.startColor = pygame.Color(10, 0, 10)
        self.endColor = pygame.Color(50, 0, 50)

        self.lerp = 0.0
        self.dir = False

        self.particles = []

        for particle in range(30):
            self.particles.append(Particle(self.elipseRect.center, randint(10, 25)))

        #rect to use to check if player collide with player
        self.posRect = self.elipseRect.copy()
        self.position = pygame.Vector2(position)

        self.surf = pygame.Surface((52, 52), pygame.SRCALPHA)

        self.offset = 0
        self.moving_up = True

    def draw(self, screen, camera_pos):
        self.surf.fill((0, 0, 0, 0))
        self.posRect = self.elipseRect.copy()
        self.posRect.topleft += self.position - camera_pos

        if not self.dir:
            self.lerp += 0.01
            if self.lerp >= 0.99:
                self.dir = True
        else:
            self.lerp -= 0.01
            if self.lerp <= 0.01:
                self.dir = False

        lerpColor = self.startColor.lerp(self.endColor, self.lerp)
        pygame.draw.ellipse(self.surf, lerpColor, self.elipseRect)
        pygame.draw.ellipse(self.surf, (0, 0, 0), self.elipseRect, 2)

        for particle in self.particles:
            particle.draw(self.surf)

            if particle.dead:
                particle.distance = 20
                particle.angle = randint(0, 360)
                particle.dead = False
        

        #pygame.draw.rect(screen, (255, 0, 0), self.posRect)

        if self.moving_up:
            self.offset -= .1
        else:
            self.offset += .1

        if self.offset <= 0:
            self.moving_up = False
        if self.offset >= 10:
            self.moving_up = True


        self.posRect = pygame.Rect(self.posRect.x, self.posRect.y+self.offset, self.posRect.width, self.posRect.height)
        screen.blit(self.surf, self.posRect.topleft)

    def place_portal(self, minPos, maxPos, tileSize, tiles):
        '''
        choose random pos
        if portal doesn't collide with any rects - place
        if collide - repeat
        '''
        
        found = False
        while not found:
            randomPos = [randint(minPos[0] * tileSize, maxPos[0] * tileSize), randint(minPos[1] * tileSize ,maxPos[1] * tileSize)]
            checkRect = self.elipseRect.copy()
            checkRect.topleft += pygame.Vector2(randomPos)

            collide = False
            for tile in tiles:
                if checkRect.colliderect(tile.rect):
                    randomPos = [randint(minPos[0] * tileSize, maxPos[0] * tileSize), randint(minPos[1] * tileSize, maxPos[1] * tileSize)]
                    checkRect = self.elipseRect.copy()
                    checkRect.topleft += pygame.Vector2(randomPos)

                    collide = True


            if not collide:
                self.position = randomPos
                self.posRect.topleft = randomPos
                
                break