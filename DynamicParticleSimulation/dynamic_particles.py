#!usr/bin/python3
from random import randint
import math
import pygame
from pygame import Vector2, Color, Surface
import sys


SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
BG_COLOR: Color = Color((135, 233, 169))
FPS: int = 360


def solve_quadratic_formula(a: float, b: float, c: float) -> Vector2:
    """
    x = -b +- sqrt(b**2 - 4ac) / 2a
    """
    if a == 0:
        return Vector2()

    bb4ac: float = (b * b) - (4 * a * c)
    if bb4ac >= 0:
        sqrt_part = math.sqrt(bb4ac)
        x1: float = (-b + sqrt_part) / (2*a)
        x2: float = (-b - sqrt_part) / (2*a)
        return Vector2(x1, x2)
    else:
        return Vector2()


class Particle:
    def __init__(
            self,
            pos: Vector2,
            vel: Vector2,
            acc: Vector2,
            radius: float,
            mass: float = None,
            color: Color = None
    ) -> None:
        # position
        self.pos: Vector2 = pos

        # forces action on particle
        self.vel: Vector2 = vel
        self.acc: Vector2 = acc

        # mass of particle required for elastic collisions
        self.mass: float = mass if mass is not None else radius**2 * math.pi

        # radius of particle
        self.radius: float = radius

        # color of particle
        self.color: Color = color if color is not None else Color('darkgreen')

    def update(self, dt: float) -> None:
        """Update particle's position and velocity based on delta time."""
        self.vel += self.acc * dt
        self.pos += self.vel * dt

    def handle_walls(self):
        """Handle collision with teh 4 static walls of the screen."""
        # helper function
        def correct_clipping(border: float, axis: int) -> None:
            """
            # axis is subscripted due to universality (khm...very useful namespaces)
            # |x is 0|
            # |y is 1|
            """
            # lazy linear interpolation idk...
            clipping: float = border - self.pos[axis]  # amount of clipping between the wall and the particle
            self.pos[axis] += 2 * clipping  # make position correct
            self.vel[axis] *= -1  # no energy loss == 100% reflection (flip axis)

        # constrain maximums (minimums are self.radius)
        x_border: float = SCREEN_WIDTH - self.radius
        y_border: float = SCREEN_HEIGHT - self.radius

        # x axis reflection
        if self.pos.x >= x_border:
            correct_clipping(x_border, 0)
        if self.pos.x <= self.radius:
            correct_clipping(self.radius, 0)

        # y axis reflection
        if self.pos.y >= y_border:
            correct_clipping(y_border, 1)
        if self.pos.y <= self.radius:
            correct_clipping(self.radius, 1)

    def draw(self, screen: Surface, draw_vectors: bool = False) -> None:
        """Draw particle onto a surface. Force vectors are optional."""
        # # draw particle itself
        pygame.draw.circle(
            screen,
            self.color,
            self.pos,
            self.radius,
        )

        if draw_vectors:
            # to make lines longer
            scale: float = math.pi
            # width of lines
            width: int = 5
            # draw velocity vector
            pygame.draw.line(
                screen,
                Color('red'),
                self.pos,
                self.pos + self.vel * 2,
                width
            )

            # draw acceleration vector
            pygame.draw.line(
                screen,
                Color('blue'),
                self.pos,
                self.pos + self.acc*2,
                width
            )

    def __str__(self):
        return f'Particle<pos=({self.pos.x}, {self.pos.y}), radius={self.radius}>'


class ParticleGroup:

    def __init__(self, number_of_particles: int):
        self.particle_list: list[Particle] = []
        self._generate_particles(number_of_particles)

    def _generate_particles(self, n: int) -> None:
        """Generate n particles."""
        for _ in range(n):
            p: Particle = Particle(
                # pos=Vector2(randint(0, SCREEN_WIDTH), randint(0, SCREEN_HEIGHT - 100)),
                pos=Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
                vel=Vector2(randint(-300, 390), randint(-300, 300)),
                acc=Vector2(0, 0),
                mass=10,
                radius=10
            )
            self.particle_list.append(p)

    @staticmethod
    def is_collision(a: Particle, b: Particle) -> bool:
        """Detect collision between to circle/particle."""
        return a.pos.distance_to(b.pos) <= a.radius + b.radius

    @staticmethod
    def resolve_collision(a: Particle, b: Particle) -> None:
        """Solve collisions for two collided circle/particle calculating TimeOfImpact (TOI)."""
        # Find the root of this function.
        # f(t) = ||distance_v - t*velocity_v|| - total_radius = 0
        # with that t the time of impact can be calculated
        distance_v: Vector2 = a.pos - b.pos
        velocity_v: Vector2 = b.vel - a.vel
        total_radius: float = a.radius + b.radius
        solutions: Vector2 = solve_quadratic_formula(
            a=velocity_v.magnitude_squared(),
            b=2 * distance_v.dot(velocity_v),
            c=distance_v.magnitude_squared() - total_radius ** 2
        )

        # choosing between the two solution of the quadratic formula
        delta_t = solutions.x if solutions.x > 0 else solutions.y
        # reset position where they were at the time of impact
        a.update(-delta_t)
        b.update(-delta_t)

        # calculate new velocities
        # https://en.wikipedia.org/wiki/Elastic_collision#Two-dimensional_collision_with_two_moving_objects
        total_mass: float = a.mass + b.mass
        distance_ab: Vector2 = a.pos - b.pos
        distance_ba: Vector2 = b.pos - a.pos
        new_vel_a: Vector2 = a.vel - (2 * b.mass / total_mass) * ((a.vel - b.vel).dot(distance_ab) / distance_ab.magnitude_squared()) * distance_ab
        new_vel_b: Vector2 = b.vel - (2 * a.mass / total_mass) * ((b.vel - a.vel).dot(distance_ba) / distance_ba.magnitude_squared()) * distance_ba

        # update velocities
        a.vel = new_vel_a
        b.vel = new_vel_b

        # go forward in time with new velocities to roll back from time of impact
        a.update(delta_t)
        b.update(delta_t)

    def update(self, dt: float) -> None:
        """Update all particle in the group."""
        # update position and velocity
        for particle in self.particle_list:
            particle.update(dt)
            # constrains particles within the screen
            particle.handle_walls()

        # check collision with every particle pair
        # its is inefficient, but the goal of this project to simulate real-ish elastic collisions between particles
        for i, a in enumerate(self.particle_list[:-1]):
            for b in self.particle_list[i+1:]:
                # check for collision
                if self.is_collision(a, b):
                    # solve collision
                    self.resolve_collision(a, b)

    def draw(self, screen: Surface, draw_vectors: bool = True) -> None:
        """Draw all particle onto a surface."""
        for particle in self.particle_list:
            particle.draw(screen, draw_vectors)


def main() -> None:
    # init pygame graphics
    pygame.init()

    # main display screen surface
    screen: Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # particle group with 100 + 1 particle
    particles: ParticleGroup = ParticleGroup(101)

    running: bool = True
    dt: float = 1 / FPS
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_a:
                    # stop continue simulation
                    running = not running

        # simulation can be turned off
        if running:
            particles.update(dt)
            screen.fill(BG_COLOR)
            particles.draw(screen, draw_vectors=False)

        # refresh screen
        pygame.display.flip()


if __name__ == '__main__':
    # even if an evil hacker hack this file with his mechanical keyboard
    # appended lines won't be executed
    sys.exit(main())
