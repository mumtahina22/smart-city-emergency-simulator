# ==============================================================
#   Smart City Emergency Simulator — Version 1
#   Computer Graphics Sessional Project (PyOpenGL + GLUT)
#
#   main.py — the START of the program. Run:  python main.py
#
#   Files:
#     settings.py -> fixed numbers (colors, sizes, speeds)
#     state.py    -> values that change while running
#     geometry.py -> BRAIN: pure math (transform, Bezier, circle)
#     pen.py      -> PEN: the only file that draws with OpenGL
#     scene.py    -> what the city looks like
#     logic.py    -> BRAIN: what happens every frame
#     main.py     -> opens the window and runs the loop
#
#   Controls:  P = pause/resume   A = send ambulance   C = show curve points
# ==============================================================

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import state
import scene
import logic
from settings import WIDTH, HEIGHT, GRASS, EAST_LANE_Y, WEST_LANE_Y


def display():
    # কী করছে: প্রতি frame-এ পুরো স্ক্রিন মুছে আবার সব আঁকছে (পেছন থেকে সামনে)
    # কেন লাগছে: animation মানে প্রতি সেকেন্ডে অনেকবার নতুন করে আঁকা
    # real world-এ এটা কোথায় দেখা যায়: সব ভিডিও গেম আর অ্যানিমেশন এভাবেই চলে
    glClear(GL_COLOR_BUFFER_BIT)
    scene.draw_roads()
    scene.draw_buildings()
    scene.draw_park()
    scene.draw_hospital()
    scene.draw_traffic_light(332, 348)          # for the rickshaw (top-left corner)
    scene.draw_traffic_light(450, 198)          # for the CNG (bottom-right corner)
    scene.draw_rickshaw(state.rickshaw_x, EAST_LANE_Y, 0)
    scene.draw_cng(state.cng_x, WEST_LANE_Y, 180)   # 180 degrees = facing left
    x, y, angle = logic.ambulance_pose()
    scene.draw_ambulance(x, y, angle)
    if state.show_controls:
        scene.draw_bezier_controls()
    scene.draw_hud()
    glutSwapBuffers()


def update(value):
    # কী করছে: প্রতি ৩৩ মিলিসেকেন্ডে (~৩০ বার/সেকেন্ড) সব কিছুর অবস্থা আপডেট করে আবার আঁকতে বলছে
    # কেন লাগছে: এটাই animation-এর হৃদস্পন্দন (game loop)
    # real world-এ এটা কোথায় দেখা যায়: প্রতিটা গেম ইঞ্জিনের update loop
    if not state.paused:
        state.frame += 1
        logic.update_light()
        logic.update_vehicles()
        logic.update_ambulance()
    glutPostRedisplay()
    glutTimerFunc(33, update, 0)


def keyboard(key, x, y):
    k = key.decode("utf-8", errors="ignore").lower()   # GLUT gives keys as bytes
    if k == "p":
        state.paused = not state.paused
    elif k == "a":
        logic.send_ambulance()
    elif k == "c":
        state.show_controls = not state.show_controls


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)      # DOUBLE = no flickering
    glutInitWindowSize(WIDTH, HEIGHT)
    glutInitWindowPosition(100, 50)
    glutCreateWindow(b"Smart City Emergency Simulator - V1")
    glClearColor(GRASS[0], GRASS[1], GRASS[2], 1.0)  # background = grass
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, 0, HEIGHT)                  # (0,0) = bottom-left corner
    glMatrixMode(GL_MODELVIEW)
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(33, update, 0)
    glutMainLoop()


if __name__ == "__main__":
    main()
