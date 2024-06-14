import glfw
from config import OFFSET_X, OFFSET_Y, SCALE_FACTOR

def key_callback(window, key, scancode, action, mods):
    global OFFSET_X, OFFSET_Y, SCALE_FACTOR

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_LEFT:
            OFFSET_X += 10
        elif key == glfw.KEY_RIGHT:
            OFFSET_X -= 10
        elif key == glfw.KEY_UP:
            OFFSET_Y -= 10
        elif key == glfw.KEY_DOWN:
            OFFSET_Y += 10
        elif key == glfw.KEY_Z:
            SCALE_FACTOR += 0.1  # Zoom in
        elif key == glfw.KEY_X:
            SCALE_FACTOR -= 0.1  # Zoom out
