# ==============================================================
#  logic.py — THE BRAIN, part 2 (what HAPPENS every frame)
#
#  Traffic light timing, when vehicles stop, and the
#  ambulance's journey. Pure Python; it CHANGES state.
# ==============================================================

import math
import state
from settings import *
from geometry import bezier_point, bezier_direction


def update_light():
    # কী করছে: টাইমার বাড়ায়; সময় শেষ হলে সিগন্যাল পরের রঙে যায় (GREEN -> YELLOW -> RED)
    # কেন লাগছে: ট্রাফিক সিগন্যাল অটোমেটিক বদলাতে
    # real world-এ এটা কোথায় দেখা যায়: আসল রাস্তার টাইমার-ভিত্তিক সিগন্যাল
    state.light_timer += 1
    if state.light_timer >= LIGHT_DURATION[state.light]:
        state.light = NEXT_LIGHT[state.light]
        state.light_timer = 0


def must_stop():
    # Vehicles stop on RED/YELLOW, and also give way while the ambulance is coming
    return state.light != "GREEN" or state.amb_phase == "straight"


def can_move(front, speed, stop_x, direction):
    # কী করছে: গাড়ি এক ধাপ এগোলে stop line পার হয়ে যাবে কিনা চেক করছে
    # কেন লাগছে: লাল বাতিতে গাড়ি ঠিক stop line-এর আগে থামাতে
    # real world-এ এটা কোথায় দেখা যায়: গেমে AI গাড়ির আচরণ, self-driving গাড়ির সিমুলেশন
    # direction = +1 means moving right, -1 means moving left
    if not must_stop():
        return True
    already_passed = front > stop_x if direction == 1 else front < stop_x
    if already_passed:
        return True       # already inside the junction -> keep going, don't block it
    next_front = front + speed * direction
    would_cross = next_front > stop_x if direction == 1 else next_front < stop_x
    return not would_cross


def update_vehicles():
    # rickshaw goes RIGHT; its front is 22 pixels ahead of its center
    if can_move(state.rickshaw_x + 22, RICKSHAW_SPEED, STOP_LINE_EAST, 1):
        state.rickshaw_x += RICKSHAW_SPEED
    if state.rickshaw_x > WIDTH + 40:
        state.rickshaw_x = -40            # came out on the right -> start again on the left

    # CNG goes LEFT; its front is 20 pixels ahead (to the left) of its center
    if can_move(state.cng_x - 20, CNG_SPEED, STOP_LINE_WEST, -1):
        state.cng_x -= CNG_SPEED
    if state.cng_x < -40:
        state.cng_x = WIDTH + 40


def send_ambulance():
    state.amb_phase = "straight"
    state.amb_y = HEIGHT + 60
    state.amb_t = 0.0
    state.amb_wait = 0


def update_ambulance():
    # কী করছে: অ্যাম্বুলেন্সের ৩টা ধাপ: সোজা নামা -> Bezier curve ধরে বাঁক -> হাসপাতালে থামা
    # কেন লাগছে: অ্যাম্বুলেন্সের পুরো যাত্রা নিয়ন্ত্রণ করতে (state machine)
    # real world-এ এটা কোথায় দেখা যায়: গেমে character-এর state (হাঁটা, দৌড়ানো, থামা)
    if state.amb_phase == "straight":
        state.amb_y -= AMBULANCE_SPEED
        if state.amb_y <= CURVE[0][1]:          # reached the start of the curve
            state.amb_phase = "curve"
            state.amb_t = 0.0
    elif state.amb_phase == "curve":
        state.amb_t += AMBULANCE_T_STEP
        if state.amb_t >= 1.0:                  # reached the hospital
            state.amb_t = 1.0
            state.amb_phase = "parked"
            state.amb_wait = 0
    elif state.amb_phase == "parked":
        state.amb_wait += 1
        if state.amb_wait > AMBULANCE_WAIT:     # wait a bit, then come again
            send_ambulance()


def ambulance_pose():
    # কী করছে: অ্যাম্বুলেন্স এখন কোথায় (x, y) আর কোন দিকে মুখ (angle) সেটা বের করছে
    # কেন লাগছে: সোজা রাস্তায় নিচের দিকে (-90°), বাঁকা রাস্তায় curve-এর দিক অনুযায়ী ঘোরে
    # real world-এ এটা কোথায় দেখা যায়: GPS navigation-এ গাড়ির আইকন রাস্তার দিকে ঘোরে
    if state.amb_phase == "straight":
        return CURVE[0][0], state.amb_y, -90
    t = state.amb_t if state.amb_phase == "curve" else 1.0
    x, y = bezier_point(CURVE, t)
    dx, dy = bezier_direction(CURVE, t)
    angle = math.degrees(math.atan2(dy, dx))
    return x, y, angle
