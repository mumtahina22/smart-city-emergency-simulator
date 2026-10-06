# ==============================================================
#  settings.py — ALL fixed numbers of the project
#  (colors, sizes, positions, speeds, timings)
#
#  These never change while the program runs.
#  Most "change this" requests in the viva = edit a number here.
# ==============================================================

WIDTH, HEIGHT = 800, 600

# Colors are (Red, Green, Blue), each from 0.0 to 1.0
GRASS        = (0.45, 0.72, 0.35)
ROAD         = (0.30, 0.30, 0.32)
WHITE        = (1.00, 1.00, 1.00)
BLACK        = (0.00, 0.00, 0.00)
RED          = (0.90, 0.10, 0.10)
YELLOW       = (1.00, 0.85, 0.10)
GREEN        = (0.10, 0.90, 0.20)
ORANGE       = (1.00, 0.55, 0.00)
LIGHT_OFF    = (0.20, 0.20, 0.20)
WINDOW_COLOR = (1.00, 0.95, 0.60)
PARK_GREEN   = (0.35, 0.65, 0.30)
TREE_GREEN   = (0.15, 0.50, 0.20)
TRUNK        = (0.45, 0.30, 0.15)
WATER        = (0.30, 0.60, 0.90)
CNG_GREEN    = (0.10, 0.55, 0.25)
GLASS        = (0.60, 0.85, 1.00)

# Road layout
H_ROAD_BOTTOM, H_ROAD_TOP = 260, 340    # horizontal road (y range)
V_ROAD_LEFT, V_ROAD_RIGHT = 360, 440    # vertical road (x range)

# Bangladesh drives on the LEFT side of the road
EAST_LANE_Y = 320        # vehicles going right (->) use the upper lane
WEST_LANE_Y = 280        # vehicles going left  (<-) use the lower lane
STOP_LINE_EAST = 350     # rickshaw must stop before this x
STOP_LINE_WEST = 450     # CNG must stop before this x

# 4 control points of the Bezier curve (curved road to the hospital)
CURVE = [(400, 200), (400, 110), (470, 100), (595, 100)]
CURVE_ROAD_HALF_WIDTH = 30

# Traffic signal timing (in frames; about 30 frames = 1 second)
LIGHT_DURATION = {"GREEN": 150, "YELLOW": 45, "RED": 150}
NEXT_LIGHT     = {"GREEN": "YELLOW", "YELLOW": "RED", "RED": "GREEN"}

# Speeds (pixels per frame)
RICKSHAW_SPEED   = 1.5
CNG_SPEED        = 2.5
AMBULANCE_SPEED  = 3.0
AMBULANCE_T_STEP = 0.008   # how much t grows each frame on the curve
AMBULANCE_WAIT   = 120     # frames the ambulance waits at the hospital