# ==============================================================
#  scene.py — WHAT the city looks like
#
#  Roads, buildings, park, hospital, traffic lights, vehicles.
#  Uses the pen to draw. It only READS state (never changes it).
# ==============================================================

import state
from settings import *
from geometry import rect_points, transform, bezier_point
from pen import (draw_rect, draw_circle, draw_line, draw_dashed_line,
                 draw_outline, draw_quad_strip, draw_part, draw_text)
from geometry import curved_road_edges


def draw_roads():
    # কী করছে: আড়াআড়ি রাস্তা, খাড়া রাস্তা, বাঁকা রাস্তা, মাঝের দাগ আর stop line আঁকছে
    # কেন লাগছে: পুরো শহরের কাঠামো এই রাস্তাগুলো
    # real world-এ এটা কোথায় দেখা যায়: Google Maps, OpenStreetMap
    draw_rect(0, H_ROAD_BOTTOM, WIDTH, H_ROAD_TOP - H_ROAD_BOTTOM, ROAD)
    draw_rect(V_ROAD_LEFT, 0, V_ROAD_RIGHT - V_ROAD_LEFT, HEIGHT, ROAD)

    # curved road to the hospital (Bezier) + its dashed center line
    draw_quad_strip(curved_road_edges(), ROAD)
    steps = 30
    for i in range(0, steps, 2):
        x1, y1 = bezier_point(CURVE, i / steps)
        x2, y2 = bezier_point(CURVE, (i + 1) / steps)
        draw_line(x1, y1, x2, y2, WHITE, 2)
    draw_rect(590, 70, 32, 60, ROAD)    # small driveway into the hospital

    # lane dividers
    mid_y = (H_ROAD_BOTTOM + H_ROAD_TOP) / 2
    mid_x = (V_ROAD_LEFT + V_ROAD_RIGHT) / 2
    draw_dashed_line(0, mid_y, V_ROAD_LEFT, mid_y, WHITE)
    draw_dashed_line(V_ROAD_RIGHT, mid_y, WIDTH, mid_y, WHITE)
    draw_dashed_line(mid_x, H_ROAD_TOP, mid_x, HEIGHT, WHITE)

    # stop lines
    draw_line(STOP_LINE_EAST, mid_y, STOP_LINE_EAST, H_ROAD_TOP, WHITE, 4)
    draw_line(STOP_LINE_WEST, H_ROAD_BOTTOM, STOP_LINE_WEST, mid_y, WHITE, 4)


def draw_building(x, y, w, h, color):
    # কী করছে: রঙিন দেয়াল, কালো আউটলাইন, আর nested loop দিয়ে সারি সারি জানালা আঁকছে
    # কেন লাগছে: শহরকে শহরের মতো দেখাতে
    # real world-এ এটা কোথায় দেখা যায়: SimCity / Cities: Skylines-এর মতো city-builder গেম
    draw_rect(x, y, w, h, color)
    draw_outline(rect_points(x, y, x + w, y + h), BLACK, 2)
    for wx in range(x + 12, x + w - 20, 28):
        for wy in range(y + 15, y + h - 25, 32):
            draw_rect(wx, wy, 14, 18, WINDOW_COLOR)


def draw_buildings():
    draw_building(30, 390, 130, 160, (0.85, 0.55, 0.35))
    draw_building(185, 370, 130, 190, (0.55, 0.60, 0.80))
    draw_building(30, 40, 150, 180, (0.90, 0.75, 0.45))
    draw_text(80, 228, "SCHOOL")
    draw_building(215, 60, 110, 140, (0.75, 0.45, 0.55))
    draw_text(238, 208, "TEA STALL")


def draw_park():
    # কী করছে: সবুজ মাঠ, বৃত্ত দিয়ে পুকুর আর গাছ আঁকছে
    # কেন লাগছে: শহরে খোলা জায়গা দেখাতে, আর বৃত্ত আঁকার ব্যবহার দেখাতে
    # real world-এ এটা কোথায় দেখা যায়: ম্যাপে পার্ক/সবুজ এলাকা
    draw_rect(470, 370, 300, 200, PARK_GREEN)
    draw_outline(rect_points(470, 370, 770, 570), BLACK, 2)
    draw_circle(640, 450, 45, WATER)
    trees = [(510, 410), (520, 520), (590, 540), (720, 520), (730, 400), (560, 470)]
    for (tx, ty) in trees:
        draw_rect(tx - 3, ty - 18, 6, 18, TRUNK)
        draw_circle(tx, ty, 16, TREE_GREEN)
    draw_text(485, 552, "PARK")


def draw_hospital():
    # কী করছে: সাদা বিল্ডিং, লাল ক্রস, দরজা আর নাম আঁকছে
    # কেন লাগছে: অ্যাম্বুলেন্সের গন্তব্য
    # real world-এ এটা কোথায় দেখা যায়: ম্যাপ অ্যাপে হাসপাতালের আইকন
    x, y, w, h = 620, 30, 160, 150
    draw_rect(x, y, w, h, (0.95, 0.95, 0.95))
    draw_outline(rect_points(x, y, x + w, y + h), BLACK, 2)
    draw_rect(690, 70, 20, 60, RED)                   # red cross (vertical bar)
    draw_rect(670, 90, 60, 20, RED)                   # red cross (horizontal bar)
    draw_rect(620, 85, 8, 30, (0.30, 0.50, 0.80))     # entrance door
    draw_text(668, 155, "HOSPITAL", RED)


def draw_traffic_light(x, y):
    # কী করছে: সিগন্যাল বক্স আর ৩টা বাতি আঁকছে; যেটা চালু সেটা উজ্জ্বল, বাকিগুলো কালচে
    # কেন লাগছে: গাড়ি কখন থামবে বা চলবে সেটা স্ক্রিনে দেখাতে
    # real world-এ এটা কোথায় দেখা যায়: ট্রাফিক সিমুলেশন সফটওয়্যার (SUMO), শহরের কন্ট্রোল রুম
    draw_rect(x, y, 20, 56, BLACK)
    red_color    = RED    if state.light == "RED"    else LIGHT_OFF
    yellow_color = YELLOW if state.light == "YELLOW" else LIGHT_OFF
    green_color  = GREEN  if state.light == "GREEN"  else LIGHT_OFF
    draw_circle(x + 10, y + 45, 7, red_color)
    draw_circle(x + 10, y + 28, 7, yellow_color)
    draw_circle(x + 10, y + 11, 7, green_color)


# ---------------- Vehicles ----------------
# Every vehicle is designed around (0, 0) facing RIGHT (angle 0).
# transform() then rotates it and moves it to (x, y).

def draw_rickshaw(x, y, angle):
    # কী করছে: (0,0)-এর চারপাশে রিকশার অংশগুলো আঁকে, তারপর transform দিয়ে আসল জায়গায় বসায়
    # কেন লাগছে: একই ডিজাইন বারবার ব্যবহার করা যায়, শুধু x, y, angle বদলালেই হয়
    # real world-এ এটা কোথায় দেখা যায়: গেমে একই গাড়ির মডেল অনেক জায়গায় দেখানো
    dark = (0.15, 0.15, 0.15)
    draw_part(rect_points(-16, -14, -6, -10), dark, x, y, angle)                 # rear wheel
    draw_part(rect_points(-16, 10, -6, 14), dark, x, y, angle)                   # rear wheel
    draw_part(rect_points(14, -2, 22, 2), dark, x, y, angle)                     # front wheel
    draw_part(rect_points(-8, -2, 16, 2), (0.50, 0.50, 0.50), x, y, angle)       # frame
    draw_part(rect_points(4, -5, 11, 5), (0.45, 0.25, 0.10), x, y, angle)        # driver seat
    draw_part(rect_points(-20, -11, -2, 11), (0.85, 0.15, 0.45), x, y, angle)    # colorful hood
    draw_part(rect_points(-15, -11, -9, 11), YELLOW, x, y, angle)                # hood art stripe


def draw_cng(x, y, angle):
    # কী করছে: সবুজ CNG অটোরিকশা আঁকছে (বডি, ছাদ, সামনের কাঁচ)
    # কেন লাগছে: বাংলাদেশের রাস্তার আসল চেহারা দেখাতে
    # real world-এ এটা কোথায় দেখা যায়: ট্রাফিক সিমুলেশনে বিভিন্ন ধরনের গাড়ি
    draw_part(rect_points(-20, -12, 20, 12), CNG_GREEN, x, y, angle)             # body
    draw_part(rect_points(-17, -10, 8, 10), (0.05, 0.35, 0.15), x, y, angle)     # roof
    draw_part(rect_points(12, -9, 17, 9), GLASS, x, y, angle)                    # windshield


def draw_ambulance(x, y, angle):
    # কী করছে: অ্যাম্বুলেন্স আঁকছে; সাইরেনের লাল-নীল বাতি পালা করে জ্বলে
    # কেন লাগছে: প্রজেক্টের মূল চরিত্র — জরুরি গাড়ি হাসপাতালে যাচ্ছে
    # real world-এ এটা কোথায় দেখা যায়: জরুরি সেবার রুট প্ল্যানিং সফটওয়্যার, গেম
    blink = (state.frame // 8) % 2 == 0 and state.amb_phase != "parked"
    body = rect_points(-28, -13, 28, 13)
    draw_part(body, WHITE, x, y, angle)
    draw_outline(transform(body, angle, x, y), BLACK, 1)
    draw_part(rect_points(-28, -13, 28, -10), RED, x, y, angle)                  # side stripe
    draw_part(rect_points(-28, 10, 28, 13), RED, x, y, angle)                    # side stripe
    draw_part(rect_points(18, -11, 25, 11), GLASS, x, y, angle)                  # windshield
    draw_part(rect_points(-12, -2.5, 4, 2.5), RED, x, y, angle)                  # red cross
    draw_part(rect_points(-6.5, -8, -1.5, 8), RED, x, y, angle)                  # red cross
    siren_red  = (1.0, 0.0, 0.0) if blink else (0.4, 0.0, 0.0)
    siren_blue = (0.0, 0.3, 1.0) if not blink else (0.0, 0.1, 0.4)
    draw_part(rect_points(8, -8, 14, -2), siren_red, x, y, angle)
    draw_part(rect_points(8, 2, 14, 8), siren_blue, x, y, angle)


def draw_bezier_controls():
    # কী করছে: Bezier-এর ৪টা control point আর তাদের যোগ করা রেখা (control polygon) দেখাচ্ছে
    # কেন লাগছে: viva-তে দেখানোর জন্য curve কোন বিন্দুগুলো দিয়ে নিয়ন্ত্রিত হচ্ছে
    # real world-এ এটা কোথায় দেখা যায়: Illustrator-এর Pen tool-এর handle
    for i in range(len(CURVE) - 1):
        draw_line(CURVE[i][0], CURVE[i][1], CURVE[i + 1][0], CURVE[i + 1][1], ORANGE, 1)
    for i, (px, py) in enumerate(CURVE):
        draw_circle(px, py, 5, ORANGE)
        draw_text(px + 7, py + 7, "P" + str(i), YELLOW)


def draw_hud():
    # কী করছে: উপরে একটা কালো বার-এ সিগন্যালের অবস্থা আর কী-বোর্ড কন্ট্রোল লিখছে
    # কেন লাগছে: ডেমোর সময় দর্শক যেন বোঝে কী হচ্ছে
    # real world-এ এটা কোথায় দেখা যায়: গেমের HUD, ড্যাশবোর্ড
    draw_rect(0, 575, WIDTH, 25, (0.10, 0.10, 0.10))
    status = "PAUSED" if state.paused else state.light
    draw_text(10, 583, "Signal: " + status +
              "    |    P: pause    A: send ambulance    C: show curve points", WHITE)
