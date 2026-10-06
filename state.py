# ==============================================================
#  state.py — everything that CHANGES while the program runs
#
#  Other files use it like this:
#       import state
#       state.light = "RED"
# ==============================================================

from settings import WIDTH, HEIGHT

frame = 0                  # counts how many frames have passed
paused = False
show_controls = False      # show Bezier control points? (key C)

# traffic signal
light = "GREEN"
light_timer = 0

# vehicles (x position only; each stays in its own lane)
rickshaw_x = -40
cng_x = WIDTH + 40

# ambulance
amb_phase = "straight"     # "straight" -> "curve" -> "parked"
amb_y = HEIGHT + 60
amb_t = 0.0                # position on the Bezier curve (0 to 1)
amb_wait = 0
