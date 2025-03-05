from .helpers import path_exists

#* --- Admin ---
# admin
RUN_AS_ADMIN = True

#* --- Player ---
# x pos
X_VELOCITY = 5

# y pos
Y_VELOCITY = 5
GRAVITY = 0.5
GRAVITY_PULL = 9.81
JUMP_HEIGHT = 12

# size
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_SIZE = (PLAYER_WIDTH, PLAYER_HEIGHT)
PLAYER_WIDTH_FACTOR = 0.05
PLAYER_HEIGHT_FACTOR = 0.09

#* --- Star ---
# size
STAR_WIDTH = 50
STAR_HEIGHT = 50
STAR_SIZE = (STAR_WIDTH, STAR_HEIGHT)
STAR_WIDTH_FACTOR = 0.05
STAR_HEIGHT_FACTOR = 0.09

# time
STAR_PICKUP_EFFECT_START_AFTER = 1000

#* ------- Game -------
# -~-~- font and text -~-~-
# ~~~ font ~~~
GAME_FONT = path_exists("wobbo/assets/fonts/game_font.ttf")

# ~~~ text ~~~
# text sizes
LEVEL_TITLE_SIZE_FACTOR = 0.05
SPECS_TEXT_SIZE_FACTOR = 0.03
INSTRUCTIONS_SIZE_FACTOR = 0.03

# text effects
LEVEL_TITLE_FADE_TIME = 0
LEVEL_TITLE_FADE_SPEED = 1
TUTORIAL_FADE_SPEED = 3
INSTRUCTIONS_FADE_SPEED = 2
