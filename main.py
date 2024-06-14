import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from constants import WIDTH, HEIGHT, PLANET_COLORS
from planet import Planet

# Global variables for offset and scaling
offset_x = 0
offset_y = 0
scale_factor = 1.0
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

    sun = Planet(0, 0, 20, PLANET_COLORS['SUN'], 1.98892 * 10**30)
    sun.sun = True

    mercury = Planet(0.387 * Planet.AU, 0, 6, PLANET_COLORS['MERCURY'], 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 6, PLANET_COLORS['VENUS'], 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    earth = Planet(-1 * Planet.AU, 0, 6.5, PLANET_COLORS['EARTH'], 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 6.5, PLANET_COLORS['MARS'], 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    jupiter = Planet(-5.203 * Planet.AU, 0, 8.5, PLANET_COLORS['JUPITER'], 1.898 * 10**27)
    jupiter.y_vel = 13.07 * 1000

    saturn = Planet(-9.537 * Planet.AU, 0, 7.5, PLANET_COLORS['SATURN'], 5.683 * 10**26)
    saturn.y_vel = 9.69 * 1000

    uranus = Planet(-19.191 * Planet.AU, 0, 7.5, PLANET_COLORS['URANUS'], 8.681 * 10**25)
    uranus.y_vel = 6.81 * 1000

    neptune = Planet(-30.069 * Planet.AU, 0, 7, PLANET_COLORS['NEPTUNE'], 1.024 * 10**26)
    neptune.y_vel = 5.43 * 1000
    
    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT)
        for planet in planets:
            planet.update_position(planets)
            planet.draw(offset_x, offset_y, scale_factor)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
