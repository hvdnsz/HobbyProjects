#!usr/bin/python3
import random
from random import randint
from operator import attrgetter
import math
import pygame
from pygame import Vector2, Color, Surface
import sys


SCREEN_WIDTH: int = 800
SCREEN_HEIGHT: int = 600
BG_COLOR: Color = Color((135, 233, 169))
FPS: int = 60 * 2
NUMBER_OF_PARTICLES: int = 15


# random ranges for particle attributes
def get_random_pos() -> Vector2:
    return Vector2(randint(0, SCREEN_HEIGHT), randint(0, SCREEN_HEIGHT))


def get_random_vel() -> Vector2:
    return Vector2(randint(-30, 30), randint(-30, 30))


def get_random_radius() -> float:
    return randint(30, 40)


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


class PhysicsError(Exception):
    """Basic error class for impossible physics (e.g. zero mass or radius)"""
    pass


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

        # buffers for continuous collision detection
        self.pos_buffer: Vector2 = self.pos
        self.vel_buffer: Vector2 = self.vel

        if mass == 0 or radius == 0:
            raise PhysicsError('mass and radius have to be not zero')

        # mass of particle required for elastic collisions
        self.mass: float = mass if mass is not None else radius**2 * math.pi

        # radius of particle
        self.radius: float = radius

        # color of particle
        self.color: Color = color if color is not None else Color('darkgreen')

    def update(self, dt: float) -> None:
        """Update particle's position and velocity based on delta time."""
        # resolve buffers
        self.pos = self.pos_buffer
        self.vel = self.vel_buffer

        # update velocity
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
                self.pos + self.vel,
                width
            )

            # draw acceleration vector
            pygame.draw.line(
                screen,
                Color('blue'),
                self.pos,
                self.pos + self.acc,
                width
            )

    def __str__(self):
        return f'Particle<pos=({self.pos.x}, {self.pos.y}), radius={self.radius}>'


class ParticleGroup:

    def __init__(self) -> None:
        self.particle_list: list[Particle] = []

    @property
    def is_empty(self) -> bool:
        """Return if the ParticleGroup is empty."""
        return False if self.particle_list else True

    def add(self, p: Particle) -> None:
        if isinstance(p, Particle):
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
        collide_point_a: Vector2 = a.pos - a.vel * delta_t
        collide_point_b: Vector2 = b.pos - b.vel * delta_t

        # calculate new velocities
        # https://en.wikipedia.org/wiki/Elastic_collision#Two-dimensional_collision_with_two_moving_objects
        total_mass: float = a.mass + b.mass
        distance_ab: Vector2 = collide_point_a - collide_point_b
        distance_ba: Vector2 = collide_point_b - collide_point_a
        try:
            new_vel_a: Vector2 = a.vel - (2 * b.mass / total_mass) * ((a.vel - b.vel).dot(distance_ab) / distance_ab.magnitude_squared()) * distance_ab
            new_vel_b: Vector2 = b.vel - (2 * a.mass / total_mass) * ((b.vel - a.vel).dot(distance_ba) / distance_ba.magnitude_squared()) * distance_ba
        except ZeroDivisionError as e:
            print(collide_point_a == collide_point_b, collide_point_a)
            print(collide_point_a + a.vel * delta_t)
            print(collide_point_b + b.vel * delta_t)
            print(a.pos - b.pos)
            print(a.vel, b.vel)
            print(a.vel - b.vel)
            print(delta_t)
            sys.exit()

        # update velocities
        a.vel_buffer = new_vel_a
        b.vel_buffer = new_vel_b

        # go forward in time with new velocities to roll back from time of impact
        a.pos_buffer += a.vel_buffer * delta_t
        b.pos_buffer += b.vel_buffer * delta_t

    def update(self, dt: float) -> None:
        """Update all particle in the group."""
        # update position and velocity
        for particle in self.particle_list:
            particle.update(dt)
            # constrains particles within the screen
            particle.handle_walls()

        # # optimized collision detection (less collision check)
        self.sweep_and_prune()

    def draw(self, screen: Surface, draw_vectors: bool = True) -> None:
        """Draw all particle onto a surface."""
        for particle in self.particle_list:
            particle.draw(screen, draw_vectors)

    def sweep_and_prune(self) -> None:
        # nothing to do
        if self.is_empty:
            return

        self.particle_list.sort(key=attrgetter('pos.x'))

        groups: list[list[Particle]] = []
        last_one: Particle = self.particle_list[0]
        groups.append([last_one])
        for particle in self.particle_list[1:]:
            if last_one.pos.x + last_one.radius >= particle.pos.x - particle.radius:
                groups[-1].append(particle)
            else:
                groups.append([particle])

            last_one = particle

        for group in groups:
            self._bruteforce_collisions(group)

    def _bruteforce_collisions(self, plist: list[Particle]) -> None:
        for i, a in enumerate(plist[:-1]):
            for b in plist[i + 1:]:
                # check for collision
                if self.is_collision(a, b):
                    # solve collision
                    self.resolve_collision(a, b)


def main() -> None:
    # init pygame graphics
    pygame.init()

    # main display screen surface
    screen: Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(f'Kinetic Gas - Elastic collision - Refresh rate: {FPS}')

    # particle group with 100 + 1 particle
    particles: ParticleGroup = ParticleGroup()

    # generate particles
    for _ in range(NUMBER_OF_PARTICLES):
        particles.add(
            Particle(
                pos=get_random_pos(),
                vel=get_random_vel(),
                acc=Vector2(),
                radius=get_random_radius(),
                mass=None,
                color=None
            )
        )

    running: bool = True
    dt: float = 1 / FPS
    draw_vectors: bool = False
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
                    # toggle simulation
                    running = not running
                elif event.key == pygame.K_v:
                    # toggle drawing vectors
                    draw_vectors = not draw_vectors

        # simulation can be turned off
        if running:
            particles.update(dt)
            screen.fill(BG_COLOR)
            particles.draw(screen, draw_vectors)

        # refresh screen
        pygame.display.flip()


if __name__ == '__main__':
    # even if an evil hacker hack this file with his mechanical keyboard
    # appended lines won't be executed
    sys.exit(main())
