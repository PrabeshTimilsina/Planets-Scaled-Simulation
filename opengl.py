import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Window dimensions
WIDTH, HEIGHT = 1500, 900

# Colors
VENUS_COLOR = (1.0, 1.0, 1.0)
SUN_COLOR = (1.0, 1.0, 0.0)
MERCURY_COLOR = (0.31, 0.30, 0.32)
EARTH_COLOR = (0.39, 0.58, 0.93)
MARS_COLOR = (0.74, 0.15, 0.20)
JUPITER_COLOR = (1, 0.5, 0)
SATURN_COLOR = (0.8, 0.8, 0.8)
URANUS_COLOR = (0.5, 0.8, 0.8)
NEPTUNE_COLOR = (0.2, 0.2, 1.0)

offset_x = 0
offset_y = 0
scale_factor = 1.0

class Planet:
    AU = 149.6e6 * 1000  # 1 AU in meters
    G = 6.67428e-11  # Gravitational constant
    SCALE = 100 / AU  # Scale for visualization
    TIMESTEP = 360 * 24 # 1 day in seconds

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

    def draw(self):
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

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    for planet in planets:
        planet.update_position(planets)
        planet.draw()
    glfw.swap_buffers(window)

def key_callback(window, key, scancode, action, mods):
    global offset_x, offset_y, scale_factor

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_LEFT:
            offset_x += 10
        elif key == glfw.KEY_RIGHT:
            offset_x -= 10
        elif key == glfw.KEY_UP:
            offset_y -= 10
        elif key == glfw.KEY_DOWN:
            offset_y += 10
        elif key == glfw.KEY_Z:
            scale_factor += 0.1  # Zoom in
        elif key == glfw.KEY_X:
            scale_factor -= 0.1  # Zoom out

def main():
    global window, planets
    if not glfw.init():
        return

    window = glfw.create_window(WIDTH, HEIGHT, "Planet Simulation", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, 0, HEIGHT)
    glMatrixMode(GL_MODELVIEW)

    sun = Planet(0, 0, 20, SUN_COLOR, 1.98892 * 10**30)
    sun.sun = True

    mercury = Planet(0.387 * Planet.AU, 0, 0.5, MERCURY_COLOR, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 0.5, VENUS_COLOR, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    earth = Planet(-1 * Planet.AU, 0, 1, EARTH_COLOR, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 1, MARS_COLOR, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    jupiter = Planet(-5.203 * Planet.AU, 0, 3, JUPITER_COLOR, 1.898 * 10**27)
    jupiter.y_vel = 13.07 * 1000

    saturn = Planet(-9.537 * Planet.AU, 0, 2, SATURN_COLOR, 5.683 * 10**26)
    saturn.y_vel = 9.69 * 1000

    uranus = Planet(-19.191 * Planet.AU, 0, 2, URANUS_COLOR, 8.681 * 10**25)
    uranus.y_vel = 6.81 * 1000

    neptune = Planet(-30.069 * Planet.AU, 0, 1.5, NEPTUNE_COLOR, 1.024 * 10**26)
    neptune.y_vel = 5.43 * 1000
    
    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    while not glfw.window_should_close(window):
        glfw.poll_events()
        display()

    glfw.terminate()

if __name__ == "__main__":
    main()
