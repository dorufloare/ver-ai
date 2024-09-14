#CONSTANTS
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800

CAR_WIDTH = 17
CAR_HEIGHT = 30

CAR_START_X = 600
CAR_START_Y = 700

CAR_IMAGE_PATH = 'assets/cars/car-blue.png'
MAP_IMAGE_PATHS = [
    'assets/maps/map-0.png',
    'assets/maps/map-1.png',
]

# car mechanics

# how easily the carn turns
TURN_SPEED = 3

# how fast the car accelerates
ACCELERATION_AMOUNT = 0.05

# how fast the car breaks
BRAKE_AMOUNT = 0.2

# maximum speed a car can reach
TOP_SPEED = 5

# minimum speed 
LOWER_SPEED_LIMIT = 0.25

# speed that can cause oversteer
OVERSTEER_SPEED = 0.7 * TOP_SPEED
OVERSTEER_INTENSITY = 0.01
OVERSTEER_ANGLE = 3.14 / 4

# off-track color
OFF_TRACK_COLOR = (255, 255, 255, 255)

# track limits
IGNORE_TRACK_LIMITS = False

# sensors
SENSOR_SENSIVITY = 30
MAX_SENSOR_LENGTH = 200
SENSOR_COLOR = (0, 255, 0, 255)

# maximum time for running a generation (seconds)
GENERATION_MAX_TIME = 60
