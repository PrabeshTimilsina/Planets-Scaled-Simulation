import math
from OpenGL.GL import *
from constants import WIDTH, HEIGHT

class Planet:
    AU = 149.6e6 * 1000  # 1 AU in meters
    G = 6.67428e-11  # Gravitational constant
    SCALE = 250 / AU # Scale for visualization
    TIMESTEP = 3600 * 24  # 1 day in seconds

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, offset_x, offset_y, scale_factor):
        x = (self.x * self.SCALE * scale_factor + WIDTH / 2) + offset_x
        y = (self.y * self.SCALE * scale_factor + HEIGHT / 2) + offset_y

        if len(self.orbit) > 2:
            glBegin(GL_LINE_STRIP)
            for point in self.orbit:
                ox, oy = point
                ox = (ox * self.SCALE * scale_factor + WIDTH / 2) + offset_x
                oy = (oy * self.SCALE * scale_factor + HEIGHT / 2) + offset_y
                glVertex2f(ox, oy)
            glEnd()

        glColor3f(*self.color)
        glBegin(GL_POLYGON)
        for i in range(100):
            theta = 2.0 * 3.1415926 * i / 100
            dx = self.radius * scale_factor * math.cos(theta)
            dy = self.radius * scale_factor * math.sin(theta)
            glVertex2f(x + dx, y + dy)
        glEnd()

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))
