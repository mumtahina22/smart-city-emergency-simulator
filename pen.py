# ==============================================================
#  pen.py — THE PEN (the ONLY file that calls OpenGL drawing)
#
#  Every function here receives points/colors that Python
#  already calculated, and just puts them on the screen.
# ==============================================================

import math
from OpenGL.GL import *
from OpenGL.GLUT import *
from settings import BLACK
from geometry import rect_points, circle_points, transform


def draw_polygon(points, color):
    # কী করছে: বিন্দুগুলো যোগ করে ভেতরটা রং দিয়ে ভরে দিচ্ছে (color fill)
    # কেন লাগছে: প্রতিটা ভরাট আকৃতি (বিল্ডিং, গাড়ি, বৃত্ত) এই একটা ফাংশন দিয়েই আঁকা হয়
    # real world-এ এটা কোথায় দেখা যায়: Photoshop-এ shape fill, ম্যাপে রঙিন এলাকা
    glColor3f(*color)
    glBegin(GL_POLYGON)
    for (x, y) in points:
        glVertex2f(x, y)
    glEnd()


def draw_outline(points, color, width=1):
    # কী করছে: আকৃতির শুধু বাইরের সীমানা রেখা আঁকছে (ভেতরে রং ছাড়া)
    # কেন লাগছে: বিল্ডিং আর গাড়ির কিনারা পরিষ্কার দেখাতে
    # real world-এ এটা কোথায় দেখা যায়: CAD সফটওয়্যার, নকশার ব্লুপ্রিন্ট
    glLineWidth(width)
    glColor3f(*color)
    glBegin(GL_LINE_LOOP)
    for (x, y) in points:
        glVertex2f(x, y)
    glEnd()


def draw_line(x1, y1, x2, y2, color, width=2):
    # কী করছে: দুইটা বিন্দুর মাঝে একটা সোজা রেখা আঁকছে
    # কেন লাগছে: রাস্তার দাগ, stop line, curve-এর control line আঁকতে
    # real world-এ এটা কোথায় দেখা যায়: Google Maps-এ রাস্তা, vector graphics
    glLineWidth(width)
    glColor3f(*color)
    glBegin(GL_LINES)
    glVertex2f(x1, y1)
    glVertex2f(x2, y2)
    glEnd()


def draw_quad_strip(edge_pairs, color):
    # কী করছে: বাম-ডান কিনারার বিন্দুগুলো জোড়ায় জোড়ায় যোগ করে একটানা চারকোণা টুকরো দিয়ে ভরাট করছে
    # কেন লাগছে: বাঁকা রাস্তার গা ভরাট করতে
    # real world-এ এটা কোথায় দেখা যায়: গেমে রাস্তা, নদী, ট্রেইল আঁকা
    glColor3f(*color)
    glBegin(GL_QUAD_STRIP)
    for (left, right) in edge_pairs:
        glVertex2f(*left)
        glVertex2f(*right)
    glEnd()


def draw_text(x, y, text, color=BLACK):
    # কী করছে: স্ক্রিনের (x, y) জায়গায় লেখা বসাচ্ছে
    # কেন লাগছে: হাসপাতাল, পার্কের নাম আর সিগন্যালের অবস্থা দেখাতে
    # real world-এ এটা কোথায় দেখা যায়: ম্যাপে জায়গার নাম, গেমের স্কোর
    glColor3f(*color)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(ch))


# ---------- small helpers built on the functions above ----------

def draw_rect(x, y, w, h, color):
    draw_polygon(rect_points(x, y, x + w, y + h), color)


def draw_circle(cx, cy, r, color):
    draw_polygon(circle_points(cx, cy, r), color)


def draw_part(local_points, color, x, y, angle):
    # কী করছে: গাড়ির একটা অংশকে (0,0) থেকে transform করে আসল জায়গায় আঁকছে
    # কেন লাগছে: প্রতিটা গাড়ির সব অংশ একসাথে নড়ে আর ঘোরে
    # real world-এ এটা কোথায় দেখা যায়: গেম ইঞ্জিনে parent-child object
    draw_polygon(transform(local_points, angle, x, y), color)


def draw_dashed_line(x1, y1, x2, y2, color, dash=20, gap=15, width=2):
    # কী করছে: একটা লম্বা রেখাকে ছোট ছোট টুকরো করে, মাঝে ফাঁকা রেখে আঁকছে
    # কেন লাগছে: রাস্তার মাঝের সাদা ভাঙা দাগ (lane divider)
    # real world-এ এটা কোথায় দেখা যায়: আসল রাস্তার lane marking, ম্যাপ অ্যাপ
    length = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / length, (y2 - y1) / length    # 1-pixel step in the line's direction
    d = 0
    while d < length:
        end = min(d + dash, length)
        draw_line(x1 + ux * d, y1 + uy * d, x1 + ux * end, y1 + uy * end, color, width)
        d += dash + gap
