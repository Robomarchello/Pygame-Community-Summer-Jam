import pygame

from scripts.entity import Entity

class ParticleManager:
    def __init__(self):
        self.particles = []

    def manage_particles(self, display, camera):
        for particle in self.particles:
            if particle.size <= 0:
                self.particles.remove(particle)
            particle.draw(display, camera)


class Particle(Entity):
    def __init__(self, x, y, speed, x_direction, y_vel, decrease_y_vel, size, decrease_size):
        super().__init__(x, y)

        self.speed = speed
        self.x_direction = x_direction
        self.y_vel = y_vel
        self.decrease_y_vel = decrease_y_vel
        self.size = size
        self.decrease_size = decrease_size

    def update_pos(self):
        self.x += self.x_direction
        if self.decrease_y_vel:
            self.y_vel += -self.speed/2

        if self.decrease_size:
            self.size -= self.speed/20

    def draw(self, display, camera):
        self.update_pos()
        pygame.draw.circle(display, (255, 255, 255), (self.x-camera.x, self.y-camera.y-self.y_vel), self.size)
