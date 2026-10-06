# ==============================================================
#  geometry.py — THE BRAIN (pure Python math)
#
#  No OpenGL in this file at all. Every function here only
#  calculates points. You could run this file without OpenGL.
# ==============================================================

import math
from settings import CURVE, CURVE_ROAD_HALF_WIDTH


def rect_points(x1, y1, x2, y2):
    # কী করছে: একটা আয়তক্ষেত্রের ৪টা কোণার (x, y) লিস্ট বানাচ্ছে
    # কেন লাগছে: রাস্তা, বিল্ডিং, গাড়ির অংশ — সবই আয়তক্ষেত্র দিয়ে তৈরি
    # real world-এ এটা কোথায় দেখা যায়: Google Maps-এ বিল্ডিং ব্লক, অ্যাপের বাটন
    return [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]


def circle_points(cx, cy, r, n=24):
    # কী করছে: বৃত্তের পরিধির উপর n টা বিন্দু বের করছে (cos আর sin দিয়ে)
    # কেন লাগছে: OpenGL-এ সরাসরি বৃত্ত আঁকার ফাংশন নেই, তাই অনেকগুলো বিন্দু যোগ করে বৃত্ত বানাই
    # real world-এ এটা কোথায় দেখা যায়: গেমে চাকা, ম্যাপে লোকেশন মার্কার
    points = []
    for i in range(n):
        angle = 2 * math.pi * i / n
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    return points


def transform(points, angle_deg, tx, ty):
    # কী করছে: প্রতিটা বিন্দুকে আগে ঘোরাচ্ছে (rotation), তারপর সরাচ্ছে (translation)
    # কেন লাগছে: গাড়ি একবার (0,0)-এর চারপাশে ডিজাইন করি, তারপর এই ফাংশন দিয়ে যেকোনো জায়গায়, যেকোনো দিকে বসাই
    # real world-এ এটা কোথায় দেখা যায়: গেম ইঞ্জিনে character নড়ানো-ঘোরানো, অ্যানিমেশন সফটওয়্যার
    a = math.radians(angle_deg)
    cos_a, sin_a = math.cos(a), math.sin(a)
    result = []
    for (x, y) in points:
        # rotation formula
        new_x = x * cos_a - y * sin_a
        new_y = x * sin_a + y * cos_a
        # translation
        result.append((new_x + tx, new_y + ty))
    return result


def bezier_point(p, t):
    # কী করছে: cubic Bezier formula দিয়ে t (0 থেকে 1) এর জন্য curve-এর উপর একটা বিন্দু বের করছে
    # কেন লাগছে: বাঁকা রাস্তা আঁকতে আর অ্যাম্বুলেন্সকে মসৃণভাবে বাঁক নেওয়াতে
    # real world-এ এটা কোথায় দেখা যায়: ফন্ট ডিজাইন, Illustrator/Photoshop-এর Pen tool, গাড়ির বডি ডিজাইন
    u = 1 - t
    x = (u**3) * p[0][0] + 3 * (u**2) * t * p[1][0] + 3 * u * (t**2) * p[2][0] + (t**3) * p[3][0]
    y = (u**3) * p[0][1] + 3 * (u**2) * t * p[1][1] + 3 * u * (t**2) * p[2][1] + (t**3) * p[3][1]
    return (x, y)


def bezier_direction(p, t):
    # কী করছে: curve-এর ওই বিন্দুতে রাস্তা কোন দিকে যাচ্ছে (derivative / tangent) সেটা বের করছে
    # কেন লাগছে: অ্যাম্বুলেন্সের মুখ যেন সবসময় রাস্তার দিকে থাকে, আর বাঁকা রাস্তার দুই পাশ বের করতে
    # real world-এ এটা কোথায় দেখা যায়: রেসিং গেমে গাড়ি ট্র্যাক ধরে ঘোরে
    u = 1 - t
    dx = 3 * (u**2) * (p[1][0] - p[0][0]) + 6 * u * t * (p[2][0] - p[1][0]) + 3 * (t**2) * (p[3][0] - p[2][0])
    dy = 3 * (u**2) * (p[1][1] - p[0][1]) + 6 * u * t * (p[2][1] - p[1][1]) + 3 * (t**2) * (p[3][1] - p[2][1])
    return (dx, dy)


def curved_road_edges(steps=30):
    # কী করছে: Bezier curve-এর প্রতিটা বিন্দু থেকে দুই পাশে (লম্ব দিকে) সরে রাস্তার বাম আর ডান কিনারা বের করছে
    # কেন লাগছে: শুধু একটা রেখা না, চওড়া একটা বাঁকা রাস্তা বানাতে
    # real world-এ এটা কোথায় দেখা যায়: Google Maps-এ চওড়া বাঁকা রাস্তা, রেসিং গেমের ট্র্যাক
    edges = []
    for i in range(steps + 1):
        t = i / steps
        x, y = bezier_point(CURVE, t)
        dx, dy = bezier_direction(CURVE, t)
        length = math.hypot(dx, dy)
        nx, ny = -dy / length, dx / length     # perpendicular (normal) direction
        left  = (x + nx * CURVE_ROAD_HALF_WIDTH, y + ny * CURVE_ROAD_HALF_WIDTH)
        right = (x - nx * CURVE_ROAD_HALF_WIDTH, y - ny * CURVE_ROAD_HALF_WIDTH)
        edges.append((left, right))
    return edges
